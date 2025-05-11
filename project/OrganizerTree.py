import tkinter as tk

from OrganizerRelatedFiles import OrganizerRelatedFiles 

# Операции со списком дерева
class OrganizerTree:
    def __init__(self, ui):
        self.ui = ui  # Сохраняем ссылку на FileTreeEditor
        self.OrganizerRelatedFiles = OrganizerRelatedFiles(ui)
        self.fontSize = 9

    # Добавить файл в список дерева
    def add_file(self):
        selected_item = self.ui.tree.focus()
        parent = selected_item if selected_item else ""
        new_item = self.ui.tree.insert(parent, "end", text="Новый файл", image=self.ui.file_icon)
        tag_name = f"tag_{new_item}" # Уникальный тег для файла
        self.ui.tree.item(new_item, tags=(tag_name,))
        self.ui.descriptions[new_item] = ""
        self.ui.icons[new_item] = "file"
        self.ui.file_links[new_item] = []  # Добавляем новый элемент в словарь связей
        self.ui.tree_structure[new_item] = (parent, "Новый файл")
        self.ui.tree.item(parent, open=True)
        self.ui.tree.focus(new_item)  # Фокус на новый элемент
        self.ui.tree.selection_set(new_item)  # Выделяем новый элемент
        self.resort_children(parent_id=parent)

    # Добавить папку в список дерева
    def add_folder(self):
        selected_item = self.ui.tree.focus()
        parent = selected_item if selected_item else ""
        new_item = self.ui.tree.insert(parent, "end", text="Новая папка", image=self.ui.folder_icon)
        tag_name = f"tag_{new_item}" # Уникальный тег для папки
        self.ui.tree.item(new_item, tags=(tag_name,))

        self.ui.descriptions[new_item] = ""
        self.ui.icons[new_item] = "folder"
        self.ui.file_links[new_item] = []  # Добавляем новый элемент в словарь связей
        self.ui.tree_structure[new_item] = (parent, "Новая папка")
        self.ui.tree.item(parent, open=True)
        self.ui.tree.focus(new_item)  # Фокус на новый элемент
        self.ui.tree.selection_set(new_item)  # Выделяем новый элемент
        self.resort_children(parent_id=parent)

    # Показывает информацию о выбранном элементе дерева в полях справа
    def on_tree_select(self, event):
        selected_item = self.ui.tree.focus()

        # Сначала сохраняем описание старого элемента
        if self.ui.last_selected_item:
            text = self.ui.description_text.get("1.0", tk.END).strip()
            self.ui.descriptions[self.ui.last_selected_item] = text

        # Обновляем выбранный элемент
        if selected_item:
            current_name = self.ui.tree.item(selected_item, "text")
            self.ui.name_entry.delete(0, tk.END)
            self.ui.name_entry.insert(0, current_name)

            desc = self.ui.descriptions.get(selected_item, "")
            self.ui.description_text.delete("1.0", tk.END)
            self.ui.description_text.insert(tk.END, desc)

            # Обновляем связи для выбранного элемента
            self.OrganizerRelatedFiles.update_link_display(selected_item)

            # Обновляем активность кнопок
            node_type = self.ui.icons.get(selected_item, "Other")
            if node_type == "file":
                self.ui.add_file_button.configure(state="disabled")
                self.ui.add_folder_button.configure(state="disabled")
                #self.add_link_button.configure(state="normal")  # Из за этого происходит дергание
                #self.remove_link_button.configure(state="normal")
            else:
                self.ui.add_file_button.configure(state="normal")
                self.ui.add_folder_button.configure(state="normal")
                #self.add_link_button.configure(state="disabled")
                #self.remove_link_button.configure(state="disabled") 
        else:
            # Если ничего не выбрано — кнопки активны
            self.ui.add_file_button.configure(state="normal")
            self.ui.add_folder_button.configure(state="normal")
            self.ui.name_entry.delete(0, tk.END)
            self.ui.description_text.delete("1.0", tk.END)
            self.ui.links_listbox.delete(0, tk.END)

        # Сохраняем текущий выбранный элемент для последующего сохранения
        self.ui.last_selected_item = selected_item

        # Обновляем чекпоинты согласно состоянию выбранного элемента
        if selected_item:
            state = self.ui.format_states.get(
                selected_item,
                {"bold": False, "strike": False, "faded": False}
            )
            self.ui.bold_var.set(state["bold"])
            self.ui.strike_var.set(state["strike"])
            self.ui.faded_var.set(state["faded"])

    # Снимает выделение, если ПКМ был вне элементов дерева
    def on_click_tree(self, event):
        region = self.ui.tree.identify("region", event.x, event.y)
        if region == "nothing":
            self.ui.tree.selection_remove(self.ui.tree.selection())
            self.ui.tree.focus("")  # Очистить фокус

            # Обновить состояние кнопок
            self.ui.add_file_button.configure(state="normal")
            self.ui.add_folder_button.configure(state="normal")

            # Очистить поля справа
            self.ui.name_entry.delete(0, tk.END)
            self.ui.description_text.delete("1.0", tk.END)
            self.ui.links_listbox.delete(0, tk.END)

    # Удаляет выбранный элемент дерева и все его дочерние элементы
    def delete_item(self, event=None):
        selected_items = set(self.ui.tree.selection())
        if not selected_items:
            return

        confirmation = tk.messagebox.askyesno(
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выделенные элементы?"
        )

        if not confirmation:
            return

        # Оставляем только верхнеуровневые (т.е. исключаем дочерние от уже выделенных родителей)
        def is_descendant(possible_ancestor, item):
            """Проверяет, является ли 'item' потомком 'possible_ancestor'"""
            parent = self.ui.tree.parent(item)
            while parent:
                if parent == possible_ancestor:
                    return True
                parent = self.ui.tree.parent(parent)
            return False

        top_level_items = set()
        for item in selected_items:
            if not any(is_descendant(other, item) for other in selected_items if other != item):
                top_level_items.add(item)

        unique_parents = set()

        def recursive_delete(item):
            for child in self.ui.tree.get_children(item):
                recursive_delete(child)
            self.ui.descriptions.pop(item, None)
            self.ui.icons.pop(item, None)
            self.ui.file_links.pop(item, None)
            self.ui.tree_structure.pop(item, None)

        # Удаляем только top-level элементы
        for item in top_level_items:
            parent_id = self.ui.tree.parent(item)
            unique_parents.add(parent_id)
            recursive_delete(item)
            self.ui.tree.delete(item)

        for parent_id in unique_parents:
            self.resort_children(parent_id)

        self.ui.tree.selection_remove(self.ui.tree.selection())
    
    # Переименовывает выбранный элемент дерева и обновляет структуру
    def rename_item(self, event=None):
        selected_item = self.ui.tree.focus()
        if selected_item:
            new_name = self.ui.name_entry.get()
            if new_name.strip():
                self.ui.tree.item(selected_item, text=new_name)

                # Обновляем tree_structure
                parent_id = self.ui.tree.parent(selected_item)
                self.ui.tree_structure[selected_item] = (parent_id, new_name)

                # Сортируем детей в родителе
                self.resort_children(parent_id)

    # Снимает выделение в дереве
    def on_escape(self, event):
        self.ui.tree.selection_remove(self.ui.tree.selection())  # Убираем выделение
        self.ui.tree.focus("")  # Убираем фокус
        self.ui.add_file_button.configure(state="normal")  # Восстанавливаем активность кнопок
        self.ui.add_folder_button.configure(state="normal")
        self.ui.name_entry.delete(0, tk.END)  # Очищаем поле имени
        self.ui.description_text.delete("1.0", tk.END)  # Очищаем поле описания

    # Сортировка по приниципу - папки сверху, файлы снизу, потом по алфавиту
    def resort_children(self, parent_id=""):
        children = list(self.ui.tree.get_children(parent_id))

        def sort_key(item_id):
            is_folder = self.ui.icons.get(item_id, "file") == "folder"
            text = self.ui.tree.item(item_id, "text").lower()
            return (not is_folder, text)

        sorted_children = sorted(children, key=sort_key)

        for idx, item_id in enumerate(sorted_children):
            self.ui.tree.move(item_id, parent_id, idx)

    # Ctrl + A - выделить все элементы списка
    def select_all_items(self, event=None):
        # Рекурсивно собираем все элементы
        def collect_all_items(parent=""):
            items = []
            for item in self.ui.tree.get_children(parent):
                items.append(item)
                items.extend(collect_all_items(item))
            return items

        all_items = collect_all_items()
        self.ui.tree.selection_set(all_items)
        return "break"  # Чтобы предотвратить стандартное поведение (выделение текста и т.п.)
    
    # Рекурсивное раскрытие дерева
    def expand_all(self):
        def recurse(item):
            self.ui.tree.item(item, open=True)
            for child in self.ui.tree.get_children(item):
                recurse(child)
        for root in self.ui.tree.get_children():
            recurse(root)

    # Рекурсивное сворачивание дерева
    def collapse_all(self):
        def recurse(item):
            self.ui.tree.item(item, open=False)
            for child in self.ui.tree.get_children(item):
                recurse(child)
        for root in self.ui.tree.get_children():
            recurse(root)

    # Удаляем все элементы из дерева
    def clear_tree(self):
        for item in self.ui.tree.get_children():
            self.ui.tree.delete(item)

        # Очищаем все связанные словари
        self.ui.descriptions.clear()
        self.ui.icons.clear()
        self.ui.file_links.clear()
        self.ui.tree_structure.clear()

        # Сбрасываем выбор и фокус
        self.ui.tree.selection_remove(self.ui.tree.selection())
        self.ui.tree.focus("")
        self.ui.name_entry.delete(0, tk.END)
        self.ui.description_text.delete("1.0", tk.END)
        self.ui.links_listbox.delete(0, tk.END)
        self.ui.last_selected_item = None