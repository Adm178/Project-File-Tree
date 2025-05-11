from OrganizerTree import OrganizerTree
from Other import Other

# Перемещение элементов в списке дерева
class DragAndDrop:
    def __init__(self, ui):
        self.ui = ui  # Сохраняем ссылку на FileTreeEditor
        self.OrganizerTree = OrganizerTree(ui)
        self.Other = Other(ui)

    # Начинает операцию перетаскивания элемента дерева
    def start_drag(self, event):
        self.dragging_item = self.ui.tree.identify_row(event.y)

    # Обрабатывает перемещение элемента во время перетаскивания
    def do_drag(self, event):
        if not self.dragging_item:
            return
        
        target_item = self.ui.tree.identify_row(event.y)
        if target_item and self.ui.icons.get(target_item) == "folder":
            # Если наведены на папку, запускаем таймер на раскрытие
            if self.ui.hovered_item != target_item:
                self.ui.hovered_item = target_item
                if self.ui.hover_after_id:
                    self.ui.after_cancel(self.ui.hover_after_id)
                self.ui.hover_after_id = self.ui.after(500, self.open_hovered_folder)
        else:
            # Если ушли с папки — отменяем таймер
            if self.ui.hover_after_id:
                self.ui.after_cancel(self.ui.hover_after_id)
                self.ui.hover_after_id = None
                self.ui.hovered_item = None
        
        # Снимаем старую подсветку
        if self.ui.prev_highlighted:
            existing_tags = list(self.ui.tree.item(self.ui.prev_highlighted, "tags"))
            if "highlighted" in existing_tags:
                existing_tags.remove("highlighted")
            self.ui.tree.item(self.ui.prev_highlighted, tags=tuple(existing_tags))

        # Подсвечиваем новый элемент
        if target_item:
            existing_tags = list(self.ui.tree.item(target_item, "tags"))
            if "highlighted" not in existing_tags:
                existing_tags.append("highlighted")
            self.ui.tree.item(target_item, tags=tuple(existing_tags))
            self.ui.prev_highlighted = target_item

    # Автоматически раскрывает папку под курсором при наведении во время перетаскивания
    def open_hovered_folder(self):
        if self.ui.hovered_item:
            self.ui.tree.item(self.ui.hovered_item, open=True)

    # Завершает перетаскивание и перемещает элемент в новое место
    def end_drag(self, event):
        target_item = self.ui.tree.identify_row(event.y)

        if not self.dragging_item:
            return

        # Перемещение в корень, если target_item пустой
        if not target_item:
            self.ui.tree.move(self.dragging_item, '', 'end')
            new_parent = target_item if target_item else ""
            self.OrganizerTree.resort_children(parent_id=new_parent)
        else:
            # Нельзя перетащить в файл или в самого себя
            if self.ui.icons.get(target_item) == "file" or self.dragging_item == target_item:
                self.dragging_item = None
                return

            # Нельзя перетащить внутрь своего потомка
            def is_descendant(parent, child):
                children = self.ui.tree.get_children(parent)
                for c in children:
                    if c == child or is_descendant(c, child):
                        return True
                return False

            if is_descendant(self.dragging_item, target_item):
                self.dragging_item = None
                return

            # Перемещаем внутрь папки
            self.ui.tree.move(self.dragging_item, target_item, "end")
            self.ui.tree.item(target_item, open=True)
            # Обновляем tree_structure
            new_parent = target_item if target_item else ""
            item_text = self.ui.tree.item(self.dragging_item, "text")
            self.ui.tree_structure[self.dragging_item] = (new_parent, item_text)
            # Сортируем детей нового родителя
            self.OrganizerTree.resort_children(parent_id=new_parent)

        # Снимаем подсветку
        if self.ui.prev_highlighted:
            existing_tags = list(self.ui.tree.item(self.ui.prev_highlighted, "tags"))
            if "highlighted" in existing_tags:
                existing_tags.remove("highlighted")
            self.ui.tree.item(self.ui.prev_highlighted, tags=tuple(existing_tags))

        if self.dragging_item in self.ui.format_states:
            self.Other.apply_item_styles(self.dragging_item)

        self.dragging_item = None