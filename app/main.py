import os
import subprocess
import sys

import gi
import math

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import cairo

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

BASE_DIR = resource_path(".")
ICONS_DIR = resource_path("assets/icons")


def _is_dark_theme():
    """Detecta se o tema GNOME/Zorin é escuro usando múltiplas fontes."""
    # Método 1: dconf CLI (funciona no PyInstaller, lê direto do arquivo)
    try:
        result = subprocess.run(
            ["/usr/bin/dconf", "read", "/org/gnome/desktop/interface/color-scheme"],
            capture_output=True,
            timeout=2,
            text=True
        )
        res = result.stdout.strip().strip("'")
        if res and res not in ('', 'default'):
            if "dark" in res.lower() or "prefer-dark" in res.lower():
                return True
    except Exception:
        pass

    # Método 2: GTK Settings (fallback)
    try:
        settings_gtk = Gtk.Settings.get_default()
        if settings_gtk:
            theme = settings_gtk.get_property("gtk-theme-name") or ""
            # Lista de indicadores de tema escuro
            dark_indicators = ['dark', '-dark', 'nord', 'dracula', 'tokyo', 'night', 'black']
            if theme and any(ind in theme.lower() for ind in dark_indicators):
                return True
    except Exception:
        pass

    return False


def _get_font_name():
    """Get system font from GTK settings."""
    settings = Gtk.Settings.get_default()
    return settings.get_property("gtk-font-name") or "Sans 11"


def _build_css(dark_theme: bool = True) -> bytes:
    """Build CSS that mixes user colors with system theme (dark/light)."""
    font_name = _get_font_name()

    if dark_theme:
        # Dark theme colors
        text_primary = "rgba(255, 255, 255, 0.95)"
        text_secondary = "rgba(255, 255, 255, 0.6)"
        text_tertiary = "rgba(255, 255, 255, 0.25)"
        text_quaternary = "rgba(255, 255, 255, 0.12)"
        button_bg_hover = "rgba(255, 255, 255, 0.12)"
        button_border_hover = "rgba(255, 255, 255, 0.2)"
        button_outline = "rgba(255, 255, 255, 0.3)"
        close_button_bg = "rgba(255, 255, 255, 0.06)"
        close_button_border = "rgba(255, 255, 255, 0.08)"
        close_button_color = "rgba(255, 255, 255, 0.5)"
        separator = "rgba(255, 255, 255, 0.05)"
    else:
        # Light theme colors
        text_primary = "rgba(0, 0, 0, 0.9)"
        text_secondary = "rgba(0, 0, 0, 0.7)"
        text_tertiary = "rgba(0, 0, 0, 0.4)"
        text_quaternary = "rgba(0, 0, 0, 0.2)"
        button_bg_hover = "rgba(0, 0, 0, 0.06)"
        button_border_hover = "rgba(0, 0, 0, 0.15)"
        button_outline = "rgba(0, 0, 0, 0.3)"
        close_button_bg = "rgba(0, 0, 0, 0.08)"
        close_button_border = "rgba(0, 0, 0, 0.1)"
        close_button_color = "rgba(0, 0, 0, 0.5)"
        separator = "rgba(0, 0, 0, 0.08)"

    css = f"""
* {{
    font-family: "{font_name}", sans-serif;
}}

#SessionWindow {{
    background-color: transparent;
}}

#UserLabel {{
    font-size: 16px;
    font-weight: 600;
    color: {text_primary};
    letter-spacing: 0.5px;
}}

#HeaderVersionLabel {{
    font-size: 10px;
    color: {text_tertiary};
    letter-spacing: 0.5px;
}}

#CloseButton {{
    background: {close_button_bg};
    border: 1px solid {close_button_border};
    border-radius: 50%;
    color: {close_button_color};
    padding: 0px;
    margin: 0px;
    font-size: 14px;
    min-width: 28px;
    min-height: 28px;
    transition: all 200ms ease;
}}

#CloseButton:hover, #CloseButton:focus {{
    background: #e0443e;
    color: white;
    border: 1px solid #c0392b;
    box-shadow: 0 0 10px rgba(224, 68, 62, 0.5);
    outline: 2px solid {button_outline};
    outline-offset: 2px;
}}

#HeaderSeparator, #FooterSeparator {{
    background-color: {separator};
    min-height: 1px;
}}

.session-button {{
    background: transparent;
    border: 2px solid transparent;
    border-radius: 16px;
    padding: 12px 16px;
    transition: all 200ms ease-out;
}}

.session-button:hover {{
    background-color: {button_bg_hover};
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
}}

.session-button:focus {{
    background-color: {button_bg_hover};
}}

.btn-label {{
    font-size: 14px;
    font-weight: 600;
    color: {text_primary};
    margin-top: 6px;
}}

#DescLabel {{
    font-size: 12px;
    color: {text_secondary};
    padding-top: 8px;
    margin: 8px 0 4px 0;
    font-weight: 400;
}}

#VersionLabel {{
    font-size: 10px;
    color: {text_quaternary};
    margin-top: 6px;
}}
"""
    return css.encode()

# Description shown in footer for each action
DESCRIPTIONS = {
    "shutdown": "Encerra todos os apps e desliga o computador.",
    "restart":  "Fecha tudo e reinicia o sistema do zero.",
    "logout":   "Encerra sua sessão e volta à tela de login.",
    "suspend":  "Salva o estado na memória e entra em modo de espera.",
}

class SessionMenu(Gtk.Window):
    def __init__(self, application=None):
        super().__init__(title="Sessão", application=application)
        self.set_name("SessionWindow")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_modal(True)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        # Set App Identity and Icon
        try:
            GLib.set_prgname("com.dyego.menu-logoff")
            GLib.set_application_name("Menu Logoff")
            icon_path = resource_path("assets/icons/icon-app.png")
            if os.path.exists(icon_path):
                # Use Pixbuf for more reliable icon setting
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_path)
                self.set_icon(pixbuf)
                Gtk.Window.set_default_icon(pixbuf)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        # Detect system dark/light mode
        self._dark = _is_dark_theme()

        # Enable RGBA compositing for transparent rounded window
        screen = Gdk.Screen.get_default()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
            self.set_app_paintable(True)
            self.connect("draw", self._on_draw)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(_build_css(self._dark))
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.set_margin_top(16)
        root.set_margin_bottom(20)
        root.set_margin_start(20)
        root.set_margin_end(20)
        self.add(root)

        # ── Header: version (left) + user name (centered) + close button (right) ──
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        header_box.set_name("HeaderBox")
        header_box.set_margin_bottom(12)

        # Version label (left, very subtle)
        try:
            with open(resource_path("version.txt"), "r") as f:
                version = f.read().strip()
        except:
            version = "1.0.1"

        ver_label = Gtk.Label(label=f"v{version}")
        ver_label.set_name("HeaderVersionLabel")
        ver_label.set_halign(Gtk.Align.START)
        ver_label.set_valign(Gtk.Align.CENTER)
        ver_label.set_margin_start(2)
        header_box.pack_start(ver_label, False, False, 0)

        # Spacer expander to push user label to center
        spacer1 = Gtk.Box()
        header_box.pack_start(spacer1, True, True, 0)

        # User name (centered)
        try:
            user = os.environ.get("USER", os.popen("whoami").read().strip())
        except Exception:
            user = "Usuário"

        user_label = Gtk.Label(label=user.upper())
        user_label.set_name("UserLabel")
        user_label.set_halign(Gtk.Align.CENTER)
        header_box.pack_start(user_label, False, False, 0)

        # Spacer expander to balance left side
        spacer2 = Gtk.Box()
        header_box.pack_start(spacer2, True, True, 0)

        # Close button (right)
        close_btn = Gtk.Button(label="✕")
        close_btn.set_name("CloseButton")
        close_btn.set_size_request(28, 28)
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.set_valign(Gtk.Align.CENTER)
        close_btn.connect("clicked", lambda *_: self.close_menu())
        header_box.pack_end(close_btn, False, False, 0)
        close_btn.set_margin_start(10)

        root.pack_start(header_box, False, False, 0)

        sep1 = Gtk.Separator()
        sep1.set_name("HeaderSeparator")
        root.pack_start(sep1, False, False, 0)

        # ── Action buttons (horizontal) ──
        # Order: shutdown | restart | logout | suspend
        actions = [
            ("shutdown.png", "Desligar",  "shutdown", "systemctl poweroff"),
            ("restart.png",  "Reiniciar", "restart",  "systemctl reboot"),
            ("logout.png",   "Sair",      "logout",   "gnome-session-quit --logout --no-prompt"),
            ("suspend.png",  "Suspenso",  "suspend",  "systemctl suspend -i"),
        ]

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_margin_top(18)
        hbox.set_margin_bottom(12)
        hbox.set_halign(Gtk.Align.CENTER)
        hbox.set_homogeneous(True)  # Todos os botões terão o mesmo tamanho
        hbox.connect("leave-notify-event", self.on_hbox_leave)
        root.pack_start(hbox, False, False, 0)

        self.buttons = []
        self.css_classes = []
        for icon_file, label_text, css_class, command in actions:
            btn = self._make_action_button(icon_file, label_text, css_class, command)
            hbox.pack_start(btn, True, True, 0)  # Expand e fill para distribuir espaço
            self.buttons.append(btn)
            self.css_classes.append(css_class)

        # ── Footer: separator + description label (only) ──
        sep2 = Gtk.Separator()
        sep2.set_name("FooterSeparator")
        sep2.set_margin_top(16)
        sep2.set_margin_bottom(8)
        root.pack_start(sep2, False, False, 0)

        self.desc_label = Gtk.Label()
        self.desc_label.set_name("DescLabel")
        self.desc_label.set_halign(Gtk.Align.CENTER)
        self.desc_label.set_line_wrap(True)
        self.desc_label.set_justify(Gtk.Justification.CENTER)
        self.desc_label.set_hexpand(True)
        self.desc_label.set_xalign(0.5)
        root.pack_start(self.desc_label, False, False, 0)

        self.connect("key-press-event", self.on_key_press)

        # Track focus changes to update description
        for btn in self.buttons:
            btn.connect("focus-in-event", self.on_btn_focus)
            btn.connect("enter-notify-event", self.on_btn_enter)
            btn.connect("leave-notify-event", self.on_btn_leave)

        self.show_all()

        # Default focus: Desligar (index 0)
        self.buttons[0].grab_focus()
        self._update_desc(0)

    def _on_draw(self, widget, cr):
        """Paint the rounded background manually when app_paintable=True."""
        alloc = widget.get_allocation()
        w, h = alloc.width, alloc.height
        r = 22  # border radius

        def rounded_rect(ctx):
            ctx.new_sub_path()
            ctx.arc(r,     r,     r, -math.pi, -math.pi / 2)
            ctx.arc(w - r, r,     r, -math.pi / 2, 0)
            ctx.arc(w - r, h - r, r, 0, math.pi / 2)
            ctx.arc(r,     h - r, r, math.pi / 2, math.pi)
            ctx.close_path()

        # 1) Clear entire widget area to fully transparent (required for compositor alpha)
        cr.save()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.restore()

        # 2) Paint rounded background — Solid opaque background
        cr.save()
        rounded_rect(cr)

        # Use system theme for background color - 100% opaque
        if self._dark:
            # Dark theme: dark background (preto quase puro)
            cr.set_source_rgba(20/255, 20/255, 20/255, 1.0)
        else:
            # Light theme: light gray background (matches system light theme)
            cr.set_source_rgba(250/255, 250/255, 250/255, 1.0)

        cr.fill_preserve()

        # Outer border for definition
        if self._dark:
            border_color = (1, 1, 1, 0.15)
        else:
            border_color = (0, 0, 0, 0.2)

        cr.set_source_rgba(*border_color)
        cr.set_line_width(1.5)
        cr.stroke_preserve()

        # Remove inner shine for more solid look
        cr.restore()

        # Let child widgets draw on top
        return False

    def _update_desc(self, idx):
        if idx < len(self.css_classes):
            css_class = self.css_classes[idx]
            text = DESCRIPTIONS.get(css_class, "")
            self.desc_label.set_text(text)

    def on_btn_focus(self, widget, event):
        if widget in self.buttons:
            self._update_desc(self.buttons.index(widget))

    def on_btn_enter(self, widget, event):
        """When mouse enters a button, it grabs focus to avoid double selection."""
        if widget in self.buttons:
            widget.grab_focus()
            self._update_desc(self.buttons.index(widget))

    def on_btn_leave(self, widget, event):
        """When mouse leaves a button, clear focus and description immediately."""
        self.set_focus(None)
        self.desc_label.set_text("")

    def on_hbox_leave(self, widget, event):
        """When mouse leaves the buttons area entirely, clear focus and description."""
        self.set_focus(None)
        self.desc_label.set_text("")

    def _load_icon(self, filename, size=48):
        path = os.path.join(ICONS_DIR, filename)
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size, size, True)
            return Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception:
            return Gtk.Label(label="?")

    def _make_action_button(self, icon_file, label_text, css_class, command):
        button = Gtk.Button()
        button.get_style_context().add_class("session-button")
        button.get_style_context().add_class(css_class)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect("clicked", self.on_button_clicked, command)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(12)
        vbox.set_margin_bottom(12)

        icon_widget = self._load_icon(icon_file, size=48)
        icon_widget.set_halign(Gtk.Align.CENTER)

        lbl = Gtk.Label(label=label_text)
        lbl.get_style_context().add_class("btn-label")
        lbl.set_halign(Gtk.Align.CENTER)

        vbox.pack_start(icon_widget, False, False, 0)
        vbox.pack_start(lbl, False, False, 0)
        button.add(vbox)

        return button

    def on_button_clicked(self, button, command):
        self.hide()
        # Use a slight delay to allow the window to hide before executing
        GLib.timeout_add(150, self._execute_and_quit, command)

    def _execute_and_quit(self, command):
        try:
            subprocess.Popen(command.split())
        except Exception:
            pass
        # Exit the application
        self.close_menu()
        return False

    def close_menu(self):
        """Unified method to close the application correctly."""
        if self.get_application():
            self.get_application().quit()
        else:
            self.destroy()
            if Gtk.main_level() > 0:
                Gtk.main_quit()

    def on_key_press(self, widget, event):
        key = event.keyval

        if key == Gdk.KEY_Escape:
            self.close_menu()
            return True

        if key in (Gdk.KEY_Return, Gdk.KEY_KP_Enter, Gdk.KEY_space):
            focused = self.get_focus()
            if focused:
                focused.activate()
            return True

        focused_idx = None
        for i, btn in enumerate(self.buttons):
            if btn == self.get_focus():
                focused_idx = i
                break

        if focused_idx is not None:
            if key in (Gdk.KEY_Right, Gdk.KEY_Down, Gdk.KEY_Tab):
                next_idx = (focused_idx + 1) % len(self.buttons)
                self.buttons[next_idx].grab_focus()
                self._update_desc(next_idx)
                return True
            if key in (Gdk.KEY_Left, Gdk.KEY_Up, Gdk.KEY_ISO_Left_Tab):
                prev_idx = (focused_idx - 1) % len(self.buttons)
                self.buttons[prev_idx].grab_focus()
                self._update_desc(prev_idx)
                return True

        return False


class SessionApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.dyego.menu-logoff")
        self.window = None  # Armazena referência da janela

    def do_activate(self):
        # Se janela já existe, apenas traz para frente
        if self.window is not None and self.window.get_visible():
            self.window.present()  # Traz janela para frente
            self.window.buttons[0].grab_focus()
            self.window._update_desc(0)
            return

        # Caso contrário, cria nova janela
        self.window = SessionMenu(application=self)
        self.window.show_all()
        self.window.buttons[0].grab_focus()
        self.window._update_desc(0)

        # Conecta evento destroy para limpar referência
        self.window.connect("destroy", self.on_window_destroy)

    def on_window_destroy(self, window):
        """Limpa referência quando janela é fechada"""
        self.window = None

if __name__ == "__main__":
    app = SessionApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
