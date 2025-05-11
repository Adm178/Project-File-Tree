from tkinter import filedialog
import tkinter as tk
import os
import subprocess

# Операции со связанными файлами
class OrganizerRelatedFiles: 
    def __init__(self, ui):
        self.ui = ui  # Сохраняем ссылку на FileTreeEditor

    # Указать и добавить адрес файл, которые находится на диске
    def add_link(self):
        selected_item = self.ui.tree.focus()
        if selected_item:
            # Запрашиваем путь к файлу, который нужно связать
            link = filedialog.askopenfilename(title="Выберите связанный файл")
            if link:
                # Добавляем ссылку в список связанных файлов
                if selected_item not in self.ui.file_links:
                    self.ui.file_links[selected_item] = []
                self.ui.file_links[selected_item].append(link)

                # Обновляем отображение связей
                self.update_link_display(selected_item)

    # Удалить из списка связанный файл
    def remove_link(self):
        selected_item = self.ui.tree.focus()
        if selected_item:
            # Удаляем выбранный файл из списка связанных
            selected_link = self.ui.links_listbox.get(tk.ACTIVE)
            linked_files = self.ui.file_links.get(selected_item, [])
            if selected_link in linked_files:
                linked_files.remove(selected_link)
                self.ui.file_links[selected_item] = linked_files
                self.update_link_display(selected_item)

    # Открыть связанный файл в какой-либо программе
    def open_link(self, event):
        selected_item = self.ui.tree.focus()
        if selected_item:
            # Получаем путь к выбранному связанному файлу
            selected_link = self.ui.links_listbox.get(tk.ACTIVE)
            if os.path.exists(selected_link):
                os.startfile(selected_link)  # Открываем файл с помощью системного средства

    # Обновляет список связанных файлов в правой панели
    def update_link_display(self, selected_item):
        linked_files = self.ui.file_links.get(selected_item, [])
        self.ui.links_listbox.delete(0, tk.END)
        for link in linked_files:
            self.ui.links_listbox.insert(tk.END, link)

    # Контекстное меню
    def show_link_menu(self, event):
        try:
            index = self.ui.links_listbox.nearest(event.y)
            self.ui.links_listbox.selection_clear(0, tk.END)
            self.ui.links_listbox.selection_set(index)
            self.ui.links_listbox.activate(index)
            self.ui.link_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.ui.link_menu.grab_release()

    # Открытие проводника через контекстное меню
    def open_in_explorer(self):
        selection = self.ui.links_listbox.curselection()
        if not selection:
            return
        selected_path = self.ui.links_listbox.get(selection[0])
        if os.path.exists(selected_path):
            subprocess.run(['explorer', '/select,', selected_path.replace('/', '\\')])
