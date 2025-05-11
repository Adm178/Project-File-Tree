import json
from tkinter import filedialog
import tkinter as tk

from OrganizerTree import OrganizerTree
from Other import Other 

# Операции с файлом проекта формата JSON
class OrganizerProject:
    def __init__(self, ui):
        self.ui = ui  # Сохраняем ссылку на FileTreeEditor
        self.OrganizerTree = OrganizerTree(ui)
        self.Other = Other(ui)

    # Сохранение данных проекта в файле json
    def save_project(self, event=None):
        for item in self.ui.tree.get_children(""):
            self.save_recursive(item)

        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if save_path:
            project_data = self.build_tree_dict("")
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, ensure_ascii=False, indent=4)

    # Рекурсивно сохраняет структуру дерева
    def save_recursive(self, item):
        if self.ui.tree.focus() == item:
            self.ui.descriptions[item] = self.ui.description_text.get("1.0", tk.END).strip()
        for child in self.ui.tree.get_children(item):
            self.save_recursive(child)

    # Формирует структуру json
    def build_tree_dict(self, parent):
        tree_dict = []
        for item in self.ui.tree.get_children(parent):
            item_dict = {
                "name": self.ui.tree.item(item, "text"),
                "description": self.ui.descriptions.get(item, ""),
                "type": self.ui.icons.get(item, "file"),
                "links": self.ui.file_links.get(item, []),
                "bold": self.ui.format_states.get(item, {}).get("bold", False),
                "strike": self.ui.format_states.get(item, {}).get("strike", False),
                "faded": self.ui.format_states.get(item, {}).get("faded", False),
                "children": self.build_tree_dict(item)
            }
            tree_dict.append(item_dict)
        return tree_dict

    # Загрузить проект из файла json
    def open_project(self):
        open_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not open_path:
            return

        # Предупреждение пользователю
        if self.ui.tree.get_children():  # Если дерево не пустое
            answer = tk.messagebox.askyesno(
                "Заменить текущий проект?",
                "Загрузка нового проекта удалит текущую структуру. Продолжить?"
            )
            if not answer:
                return  # Отмена загрузки 
                   
        # Очистка дерева
        self.OrganizerTree.clear_tree()

        if open_path:
            with open(open_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)
                self.build_tree_from_dict("", project_data)

    # Восстанавливает дерево из json
    def build_tree_from_dict(self, parent, data):
        for item in data:
            # Вставляем новый элемент
            new_item = self.ui.tree.insert(parent, "end", text=item["name"], image=self.ui.folder_icon if item["type"] == "folder" else self.ui.file_icon)

            # Сохраняем описание и тип
            self.ui.descriptions[new_item] = item["description"]
            self.ui.icons[new_item] = item["type"]
            self.ui.file_links[new_item] = item.get("links", [])  # Восстанавливаем связи
            self.ui.format_states[new_item] = {
                "bold": item.get("bold", False),
                "strike": item.get("strike", False),
                "faded": item.get("faded", False),
            }
            self.ui.tree_structure[new_item] = (parent, item["name"])

            self.Other.apply_item_styles(new_item)

            # Рекурсивно добавляем дочерние элементы
            if item["children"]:
                self.build_tree_from_dict(new_item, item["children"])