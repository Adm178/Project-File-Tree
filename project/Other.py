import os
from PIL import Image, ImageTk

from OrganizerRelatedFiles import OrganizerRelatedFiles 

# Остальные методы
class Other:
    def __init__(self, ui):
        self.ui = ui  # Сохраняем ссылку на FileTreeEditor
        self.OrganizerRelatedFiles = OrganizerRelatedFiles(ui)
        self.fontSize = 9
        self.font = "Segoe UI"

    # Загрузка иконки к соответсвующему элементу дерева
    def load_icon(self, filename):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, "Assets", filename)  # предполагается папка Assets/
            img = Image.open(icon_path)
            img = img.resize((16, 16), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Ошибка загрузки иконки {filename}: {e}")
            return None
        
    def update_format(self):
        item = self.ui.tree.focus()
        if not item:
            return

        tag_name = f"tag_{item}"

        state = {
        "bold": self.ui.bold_var.get(),
        "strike": self.ui.strike_var.get(),
        "faded": self.ui.faded_var.get(),
        }
        self.ui.format_states[item] = state  # Сохраняем состояние

        # Формируем стиль
        font_mods = []
        if self.ui.bold_var.get():
            font_mods.append("bold")
        if self.ui.strike_var.get():
            font_mods.append("overstrike")

        font_style = " ".join(font_mods) if font_mods else "normal"
        fg_color = "#888888" if self.ui.faded_var.get() else "#000000"

        self.ui.tree.tag_configure(tag_name, font=(self.font, self.fontSize, font_style), foreground=fg_color)
        self.ui.tree.item(item, tags=(tag_name,))

        if self.ui.apply_to_children_var.get():
            self.apply_style_to_children(item, font_style, fg_color)

    def apply_style_to_children(self, item, font_style, fg_color):
        for child in self.ui.tree.get_children(item):
            tag_name = f"tag_{child}"
            self.ui.tree.tag_configure(tag_name, font=(self.font, self.fontSize, font_style), foreground=fg_color)
            self.ui.tree.item(child, tags=(tag_name,))
            self.apply_style_to_children(child, font_style, fg_color)

    def update_format_for(self, item_id):
        style = self.ui.format_states.get(item_id, {})
        tags = []

        if style.get("bold"):
            tags.append("bold")
        if style.get("strike"):
            tags.append("strike")
        if style.get("faded"):
            tags.append("faded")

        self.ui.tree.item(item_id, tags=tuple(tags))

    def apply_item_styles(self, item_id):
        tags = []

        if self.ui.bold_flags.get(item_id):
            tags.append("bold")
        if self.ui.strike_flags.get(item_id):
            tags.append("strike")
        if self.ui.faded_flags.get(item_id):
            tags.append("faded")

        self.ui.tree.item(item_id, tags=tags)