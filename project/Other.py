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

        state = self.ui.format_states.setdefault(item, {})
        state["bold"] = self.ui.bold_var.get()
        state["strike"] = self.ui.strike_var.get()
        state["faded"] = self.ui.faded_var.get()

        font_mods = []
        if state["bold"]:
            font_mods.append("bold")
        if state["strike"]:
            font_mods.append("overstrike")

        font_style = " ".join(font_mods) if font_mods else "normal"
        fg_color = "#888888" if state["faded"] else "#000000"

        self.ui.tree.tag_configure(tag_name, font=(self.font, self.fontSize, font_style), foreground=fg_color)
        self.ui.tree.item(item, tags=(tag_name,))

    def apply_style_to_children(self, parent_item, font_style, fg_color):
        children = self.ui.tree.get_children(parent_item)

        for child in children:
            # Обновляем формат в format_states
            state = self.ui.format_states.setdefault(child, {})
            state["bold"] = "bold" in font_style
            state["strike"] = "overstrike" in font_style
            state["faded"] = fg_color == "#888888"

            # Применяем визуальный стиль
            tag_name = f"tag_{child}"
            self.ui.tree.tag_configure(tag_name, font=(self.font, self.fontSize, font_style), foreground=fg_color)
            self.ui.tree.item(child, tags=(tag_name,))

            # Рекурсивно применяем к вложенным
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

        fmt = self.ui.format_states.get(item_id, {})
        if fmt.get("bold"):
            tags.append("bold")
        if fmt.get("strike"):
            tags.append("strike")
        if fmt.get("faded"):
            tags.append("faded")

        self.ui.tree.item(item_id, tags=tags)
    
    def update_checkboxes_from_format(self, item_id):
        format_data = self.format_states.get(item_id, {})
        
        self.bold_checkbox_var.set(format_data.get("bold", False))
        self.strike_checkbox_var.set(format_data.get("strike", False))
        self.faded_checkbox_var.set(format_data.get("faded", False))

    def apply_format_to_all_children(self):
        item = self.ui.tree.focus()
        if not item:
            return

        state = self.ui.format_states.get(item, {})
        font_mods = []
        if state.get("bold"):
            font_mods.append("bold")
        if state.get("strike"):
            font_mods.append("overstrike")
        font_style = " ".join(font_mods) if font_mods else "normal"
        fg_color = "#888888" if state.get("faded") else "#000000"

        self.apply_style_to_children(item, font_style, fg_color)