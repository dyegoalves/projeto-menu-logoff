import gi
import os
import subprocess
import math

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import cairo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")


def _is_dark_theme():
    """Detect if ZorinOS / GNOME is using a dark theme using gsettings and GTK settings."""
    try:
        # Check GNOME color-scheme first (modern way)
        res = subprocess.check_output(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            stderr=subprocess.DEVNULL
        ).decode().strip().strip("'")
        if "dark" in res:
            return True
    except:
        pass

    settings = Gtk.Settings.get_default()
    if settings.get_property("gtk-application-prefer-dark-theme"):
        return True

    theme = settings.get_property("gtk-theme-name") or ""
    return "dark" in theme.lower()


def _get_font_name():
    """Get system font from GTK settings."""
    settings = Gtk.Settings.get_default()
    return settings.get_property("gtk-font-name") or "Sans 11"


def _build_css() -> bytes:
    """Build CSS that mixes user colors with Zorin system accent colors."""
    font_name = _get_font_name()
    
    # User colors
    header_side = "#2a2a2a"
    hover_color = "#3f3f3f"
    
    css = f"""
* {{
    font-family: "{font_name}", sans-serif;
}}

#SessionWindow {{
    background-color: transparent;
}}

#UserLabel {{
    font-size: 11px;
    font-weight: 700;
    color: alpha(@theme_fg_color, 0.45);
    letter-spacing: 0.8px;
}}

#CloseButton {{
    background: alpha(@theme_fg_color, 0.08);
    border: 1px solid alpha(@theme_fg_color, 0.1);
    border-radius: 50%;
    color: alpha(@theme_fg_color, 0.5);
    padding: 0px;
    margin: 0px;
    font-size: 11px;
    min-width: 24px;
    min-height: 24px;
}}

#CloseButton:hover {{
    background: #e0443e;
    color: white;
    border: 1px solid #c0392b;
}}

#HeaderSeparator, #FooterSeparator {{ 
    background-color: alpha(@theme_fg_color, 0.1); 
    min-height: 1px; 
}}

.session-button {{
    background: transparent;
    border: 2px solid transparent;
    border-radius: 18px;
    margin: 6px;
    transition: all 150ms ease;
}}

.session-button:hover, .session-button:focus {{
    background-color: #3f3f3f;
    border: 2px solid rgba(255, 255, 255, 0.1);
}}

.btn-label {{
    font-size: 12px;
    font-weight: 500;
    color: alpha(@theme_fg_color, 0.85);
}}

#DescLabel {{
    font-size: 12px;
    color: alpha(@theme_fg_color, 0.4);
    padding-top: 8px;
    margin: 14px 0 8px 0;
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
    def __init__(self):
        super().__init__(title="Sessão")
        self.set_name("SessionWindow")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_modal(True)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

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
        style_provider.load_from_data(_build_css())
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.set_margin_top(14)
        root.set_margin_bottom(18)
        root.set_margin_start(16)
        root.set_margin_end(16)
        self.add(root)

        # ── Header row: user name (centered) + X button (right) ──
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        header_box.set_name("HeaderBox")
        header_box.set_margin_bottom(12)

        try:
            user = os.environ.get("USER", os.popen("whoami").read().strip())
        except Exception:
            user = "Usuário"

        # Spacer left (same width as close button) to keep name centered
        spacer = Gtk.Box()
        spacer.set_size_request(28, 1)
        header_box.pack_start(spacer, False, False, 0)

        user_label = Gtk.Label(label=user.upper())
        user_label.set_name("UserLabel")
        user_label.set_halign(Gtk.Align.CENTER)
        header_box.pack_start(user_label, True, True, 0)

        close_btn = Gtk.Button(label="✕")
        close_btn.set_name("CloseButton")
        close_btn.set_size_request(24, 24)
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.set_valign(Gtk.Align.CENTER)
        close_btn.connect("clicked", lambda *_: Gtk.main_quit())
        header_box.pack_end(close_btn, False, False, 0)

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

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_margin_top(14)
        hbox.set_margin_bottom(6)
        hbox.set_halign(Gtk.Align.CENTER)
        hbox.connect("leave-notify-event", self.on_hbox_leave)
        root.pack_start(hbox, False, False, 0)

        self.buttons = []
        self.css_classes = []
        for icon_file, label_text, css_class, command in actions:
            btn = self._make_action_button(icon_file, label_text, css_class, command)
            hbox.pack_start(btn, False, False, 0)
            self.buttons.append(btn)
            self.css_classes.append(css_class)

        # ── Footer: separator + description label ──
        sep2 = Gtk.Separator()
        sep2.set_name("FooterSeparator")
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

        # 2) Paint rounded background — Mixture of user #1e1e1e and system alpha
        cr.save()
        rounded_rect(cr)
        
        # Solid background as requested (opacity 1.0)
        cr.set_source_rgba(30/255, 30/255, 30/255, 1.0)
        cr.fill_preserve()
        
        # Border: mix of system FG and user #2a2a2a
        cr.set_source_rgba(1, 1, 1, 0.08)
        cr.set_line_width(1.5)
        cr.stroke()
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
        vbox.set_margin_top(14)
        vbox.set_margin_bottom(14)
        vbox.set_margin_start(18)
        vbox.set_margin_end(18)

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
        GLib.timeout_add(120, lambda: (subprocess.Popen(command.split()), Gtk.main_quit()))

    def on_key_press(self, widget, event):
        key = event.keyval

        if key == Gdk.KEY_Escape:
            Gtk.main_quit()
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


if __name__ == "__main__":
    win = SessionMenu()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
