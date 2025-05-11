import tkinter as tk

# Поиск в дереве
class Search:
    def __init__(self, ui):
        self.ui = ui  # Сохраняем ссылку на FileTreeEditor

    # Фильтрует дерево по строке поиска, оставляя только совпадающие элементы
    def update_tree_filter(self, *args):
        query = self.ui.search_var.get().lower()

        # Очищаем дерево полностью
        for item in self.ui.tree.get_children():
            self.ui.tree.delete(item)

        if not query:
            # Если пустая строка поиска — восстановить всё дерево
            self.restore_full_tree()
            return

        # Находим все элементы, чье имя подходит
        matches = []
        for item_id, (parent_id, text) in self.ui.tree_structure.items():
            if query in text.lower():
                matches.append(item_id)

        # Вставляем обратно все нужные элементы и их родителей
        def insert_with_parents(item_id):
            if item_id in self.ui.tree_structure:
                parent_id, text = self.ui.tree_structure[item_id]
                if parent_id:
                    insert_with_parents(parent_id)
                if not self.ui.tree.exists(item_id):
                    if parent_id:
                        parent_tree_id = parent_id if self.ui.tree.exists(parent_id) else ""
                    else:
                        parent_tree_id = ""
                    node_type = self.ui.icons.get(item_id, "file")
                    image = self.ui.folder_icon if node_type == "folder" else self.ui.file_icon
                    self.ui.tree.insert(parent_tree_id, "end", iid=item_id, text=text, image=image)

                    if self.ui.icons.get(item_id) == "folder":
                        self.ui.tree.item(item_id, open=True)
        
        for item_id in matches:
            insert_with_parents(item_id)

    # Восстанавливает полное дерево после очищения поле поиска
    def restore_full_tree(self):
        added = set()

        def recursive_add(item_id, parent_id):
            if parent_id and parent_id not in added:
                recursive_add(parent_id, self.ui.tree_structure[parent_id][0])
            if item_id not in added:
                if parent_id:
                    parent_tree_id = parent_id if self.ui.tree.exists(parent_id) else ""
                else:
                    parent_tree_id = ""
                text = self.ui.tree_structure[item_id][1]
                node_type = self.ui.icons.get(item_id, "file")
                image = self.ui.folder_icon if node_type == "folder" else self.ui.file_icon
                self.ui.tree.insert(parent_tree_id, "end", iid=item_id, text=text, image=image)
                added.add(item_id)

        for item_id, (parent_id, _) in self.ui.tree_structure.items():
            recursive_add(item_id, parent_id)