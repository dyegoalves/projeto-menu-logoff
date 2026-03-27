import gi
import os
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")

CSS = b"""
* {
    font-family: "SF Pro Display", "Inter", "Helvetica Neue", "Segoe UI", sans-serif;
}

#SessionWindow {
    background-color: rgba(24, 24, 28, 0.94);
    border-radius: 22px;
    border: 1px solid rgba(255, 255, 255, 0.09);
}

#HeaderBox {
    padding: 0px;
}

#UserLabel {
    font-size: 12px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.40);
    letter-spacing: 0.8px;
}

#CloseButton {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 50%;
    padding: 0px;
    min-width: 24px;
    min-height: 24px;
    color: rgba(255, 255, 255, 0.50);
    font-size: 13px;
    font-weight: 600;
    outline: none;
    box-shadow: none;
}

#CloseButton:hover {
    background: rgba(255, 80, 80, 0.70);
    border: 1px solid rgba(255, 80, 80, 0.80);
    color: white;
    outline: none;
    box-shadow: none;
}

#CloseButton:focus {
    outline: none;
    box-shadow: none;
}

#HeaderSeparator {
    background-color: rgba(255, 255, 255, 0.07);
    min-height: 1px;
}

.session-button {
    background: transparent;
    border: 2px solid transparent;
    border-radius: 16px;
    padding: 0px;
    margin: 6px 4px;
    outline: none;
    box-shadow: none;
    transition: all 150ms ease;
}

.session-button:hover {
    background-color: rgba(255, 255, 255, 0.08);
    border: 2px solid rgba(255, 255, 255, 0.12);
    outline: none;
    box-shadow: none;
}

.session-button:focus {
    background-color: rgba(255, 255, 255, 0.13);
    border: 2px solid rgba(255, 255, 255, 0.55);
    outline: none;
    box-shadow: none;
}

.session-button.shutdown:focus {
    background-color: rgba(255, 107, 107, 0.18);
    border: 2px solid rgba(255, 107, 107, 0.70);
}

.session-button.restart:focus {
    background-color: rgba(6, 214, 160, 0.15);
    border: 2px solid rgba(6, 214, 160, 0.65);
}

.session-button.logout:focus {
    background-color: rgba(255, 209, 102, 0.15);
    border: 2px solid rgba(255, 209, 102, 0.65);
}

.session-button.suspend:focus {
    background-color: rgba(138, 180, 248, 0.15);
    border: 2px solid rgba(138, 180, 248, 0.65);
}

.session-button:active {
    background-color: rgba(255, 255, 255, 0.20);
}

.btn-label {
    font-size: 12px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.75);
}

#FooterSeparator {
    background-color: rgba(255, 255, 255, 0.07);
    min-height: 1px;
}

#DescLabel {
    font-size: 11px;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.35);
    margin-top: 10px;
    margin-bottom: 10px;
}
"""

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

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.set_margin_top(14)
        root.set_margin_bottom(0)
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
            ("shutdown.png", "Desligar",  "shutdown", "gnome-session-quit --power-off --no-prompt"),
            ("restart.png",  "Reiniciar", "restart",  "gnome-session-quit --reboot --no-prompt"),
            ("logout.png",   "Sair",      "logout",   "gnome-session-quit --logout --no-prompt"),
            ("suspend.png",  "Suspenso",  "suspend",  "systemctl suspend -i"),
        ]

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_margin_top(14)
        hbox.set_margin_bottom(6)
        hbox.set_halign(Gtk.Align.CENTER)
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
        root.pack_start(self.desc_label, False, False, 0)

        self.connect("key-press-event", self.on_key_press)

        # Track focus changes to update description
        for btn in self.buttons:
            btn.connect("focus-in-event", self.on_btn_focus)
            btn.connect("enter-notify-event", self.on_btn_enter)

        self.show_all()

        # Default focus: Desligar (index 0)
        self.buttons[0].grab_focus()
        self._update_desc(0)

    def _update_desc(self, idx):
        if idx < len(self.css_classes):
            css_class = self.css_classes[idx]
            text = DESCRIPTIONS.get(css_class, "")
            self.desc_label.set_text(text)

    def on_btn_focus(self, widget, event):
        if widget in self.buttons:
            self._update_desc(self.buttons.index(widget))

    def on_btn_enter(self, widget, event):
        if widget in self.buttons:
            self._update_desc(self.buttons.index(widget))

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
