import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import tkinter.font as tkfont

from Search import Search
from OrganizerTree import OrganizerTree
from OrganizerProject import OrganizerProject
from OrganizerRelatedFiles import OrganizerRelatedFiles 
from DragAndDrop import DragAndDrop 
from Other import Other 

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FileTreeEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Инициализация полей классов других файлов
        self.OrganizerTree = OrganizerTree(self)
        self.Search = Search(self)
        self.OrganizerProject = OrganizerProject(self)
        self.OrganizerRelatedFiles = OrganizerRelatedFiles(self)
        self.DragAndDrop = DragAndDrop(self)
        self.Other = Other(self)

        # Название
        self.title("Редактор структуры файлов")
        # Центрирование окна
        window_width = 800
        window_height = 600

        # Получаем размеры экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Вычисляем позицию окна, чтобы оно было по центру
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Устанавливаем новое положение окна
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.geometry("800x600")

        # Загрузка иконок
        self.folder_icon = self.Other.load_icon("folder.png")
        self.file_icon = self.Other.load_icon("file.png")

        # Настройка колонок и строк для растягивания
        self.grid_columnconfigure(0, weight=1)  # Первая колонка растягивается
        self.grid_columnconfigure(1, weight=1)  # Вторая колонка растягивается
        self.grid_rowconfigure(0, weight=0)  # Строка для дерева растягивается
        self.grid_rowconfigure(1, weight=1)  # Строка для панели справа растягивается

        # Панель для дерева и кнопок раскрытия
        self.tree_panel = ctk.CTkFrame(self)
        self.tree_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.tree_panel.grid_rowconfigure(1, weight=1)  # Дерево должно растягиваться
        self.tree_panel.grid_rowconfigure(2, weight=0)  # Строка поиска будет фиксированной
        self.tree_panel.grid_columnconfigure(0, weight=1)

        # Создание дерева
        self.tree = ttk.Treeview(self.tree_panel)

        self.default_font = tkfont.nametofont("TkDefaultFont").actual("family")
        self.default_font_size = tkfont.nametofont("TkDefaultFont").actual("size")
        self.tree.tag_configure("highlighted", background="#5555ff")
        self.tree.tag_configure("bold", font=(self.default_font, self.default_font_size, "bold"))
        self.tree.tag_configure("strike", foreground="gray", font=(self.default_font, self.default_font_size, "overstrike"))
        self.tree.tag_configure("faded", foreground="gray70")
        self.tree.grid(row=1, column=0, sticky="nsew")

        # Кнопки раскрытия / скрытия
        self.expand_collapse_frame = ctk.CTkFrame(self.tree_panel, fg_color="transparent")
        self.expand_collapse_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))

        self.expand_collapse_frame.grid_columnconfigure(0, weight=1, uniform="button")
        self.expand_collapse_frame.grid_columnconfigure(1, weight=1, uniform="button")

        self.expand_all_button = ctk.CTkButton(self.expand_collapse_frame, text="Раскрыть всё", command=self.OrganizerTree.expand_all)
        self.expand_all_button.grid(row=0, column=0, padx=5, sticky="n")

        self.collapse_all_button = ctk.CTkButton(self.expand_collapse_frame, text="Скрыть всё", command=self.OrganizerTree.collapse_all)
        self.collapse_all_button.grid(row=0, column=1, padx=5, sticky="n")

        # Привязка события для выделения
        self.tree.bind("<<TreeviewSelect>>", self.OrganizerTree.on_tree_select)
        self.bind("<Escape>", self.OrganizerTree.on_escape)

        # Правая панель с редактором
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Настройка строк и колонок правой панели для растягивания
        self.right_panel.grid_rowconfigure(0, weight=0)  # Строка с заголовками
        self.right_panel.grid_rowconfigure(1, weight=1)  # Строка с описанием растягивается
        self.right_panel.grid_rowconfigure(2, weight=0)  # Строка с меткой "Связанные файлы"
        self.right_panel.grid_rowconfigure(3, weight=0)  # Строка с links_listbox растягивается
        self.right_panel.grid_rowconfigure(4, weight=0)  # Строка с кнопками для добавления/удаления
        self.right_panel.grid_columnconfigure(0, weight=1)  # Для левого столбца
        self.right_panel.grid_columnconfigure(1, weight=1)  # Для правого столбца

        self.name_label = ctk.CTkLabel(self.right_panel, text="Имя файла/папки:")
        self.name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.name_entry = ctk.CTkEntry(self.right_panel)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.name_entry.bind("<Return>", lambda event: self.OrganizerTree.rename_item(event))
        
        # Текстбокс для описания папки/файла
        self.description_text = ctk.CTkTextbox(self.right_panel)
        self.description_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Панель кнопок
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Сделаем три колонки: левая пустая (растягивается), центр с кнопками, правая пустая (растягивается)
        self.button_frame.grid_columnconfigure(0, weight=1)  # левая
        self.button_frame.grid_columnconfigure(1, weight=0)  # центр
        self.button_frame.grid_columnconfigure(2, weight=1)  # правая

        # Центровочный фрейм внутри, где все кнопки
        self.center_buttons_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        self.center_buttons_frame.grid(row=0, column=1)  # по центру

        self.add_file_button = ctk.CTkButton(self.center_buttons_frame, text="Добавить файл", command=self.OrganizerTree.add_file)
        self.add_file_button.grid(row=0, column=0, padx=5, pady=5)

        self.add_folder_button = ctk.CTkButton(self.center_buttons_frame, text="Добавить папку", command=self.OrganizerTree.add_folder)
        self.add_folder_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = ctk.CTkButton(self.center_buttons_frame, text="Удалить", command=self.OrganizerTree.delete_item)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)  

        self.save_button = ctk.CTkButton(self.center_buttons_frame, text="Сохранить проект как", command=self.OrganizerProject.save_project)
        self.save_button.grid(row=0, column=4, padx=5, pady=5)

        self.load_button = ctk.CTkButton(self.center_buttons_frame, text="Загрузить проект", command=self.OrganizerProject.open_project)
        self.load_button.grid(row=0, column=5, padx=5, pady=5)

        # Новый интерфейс для связей
        self.links_label = ctk.CTkLabel(self.right_panel, text="Связанные файлы:")
        self.links_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        # Используем обычный Listbox для отображения связей
        self.links_listbox = tk.Listbox(self.right_panel, height=1)
        self.links_listbox.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.links_listbox.bind("<Double-1>", self.OrganizerRelatedFiles.open_link)
        self.links_listbox.bind("<Button-3>", self.OrganizerRelatedFiles.show_link_menu)

        self.link_menu = tk.Menu(self.links_listbox, tearoff=0)
        self.link_menu.add_command(label="Открыть в проводнике", command=self.OrganizerRelatedFiles.open_in_explorer)


        self.add_link_button = ctk.CTkButton(self.right_panel, text="Добавить связанный файл", command=self.OrganizerRelatedFiles.add_link)
        self.add_link_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.remove_link_button = ctk.CTkButton(self.right_panel, text="Удалить связанный файл", command=self.OrganizerRelatedFiles.remove_link)
        self.remove_link_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Строка поиска
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.Search.update_tree_filter)
        self.search_entry = ctk.CTkEntry(self.tree_panel, textvariable=self.search_var, placeholder_text="Поиск...")
        self.search_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Фрейм для чекпоинтов состояния элемента
        self.state_options_frame = ctk.CTkFrame(self.right_panel)
        self.state_options_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 10))
        self.state_options_frame.grid_columnconfigure(0, weight=1)
        self.state_options_frame.grid_columnconfigure(1, weight=1)

        self.bold_var = tk.BooleanVar()
        self.strike_var = tk.BooleanVar()
        self.faded_var = tk.BooleanVar()
        self.apply_to_children_var = tk.BooleanVar()

        self.bold_check = ctk.CTkCheckBox(self.state_options_frame, text="Жирный", variable=self.bold_var, command=self.Other.update_format)
        self.bold_check.grid(row=0, column=0, sticky="w", padx=5)

        self.strike_check = ctk.CTkCheckBox(self.state_options_frame, text="Зачёркнутый", variable=self.strike_var, command=self.Other.update_format)
        self.strike_check.grid(row=1, column=0, sticky="w", padx=5)

        self.faded_check = ctk.CTkCheckBox(self.state_options_frame, text="Блеклый", variable=self.faded_var, command=self.Other.update_format)
        self.faded_check.grid(row=2, column=0, sticky="w", padx=5)

        self.apply_to_children_check = ctk.CTkCheckBox(
            self.state_options_frame, 
            text="Применить ко всем дочерним", 
            variable=self.apply_to_children_var,
            command=self.Other.update_format
        )
        self.apply_to_children_check.grid(row=1, column=1, rowspan=3, sticky="n", padx=5)

        #-------------------------------------------------------------------------------------
        # Инициализация данных
        self.descriptions = {}
        self.icons = {}
        self.file_links = {}
        self.last_selected_item = None

        self.format_states = {}

        self.bold_flags = {}
        self.strike_flags = {}
        self.faded_flags = {}
        self.apply_to_all_flags = {}

        # Обработка кликов по дереву (снятие выделения)
        self.tree.bind("<Button-3>", self.OrganizerTree.on_click_tree, add="+")
        self.drop_position = None
        self.hover_after_id = None
        self.hovered_item = None
        self.prev_highlighted = None
        self.tree.bind("<ButtonPress-1>", self.DragAndDrop.start_drag)
        self.tree.bind("<B1-Motion>", self.DragAndDrop.do_drag)
        self.tree.bind("<ButtonRelease-1>", self.DragAndDrop.end_drag)
        self.tree.bind("<Delete>", self.OrganizerTree.delete_item)

        # Ctrl+A для выделения всех элементов дерева
        self.tree.bind("<Control-a>", self.OrganizerTree.select_all_items)
        self.tree.bind("<Control-A>", self.OrganizerTree.select_all_items)
        # Ctrl+S для открытия окна сохранения
        self.bind("<Control-s>", self.OrganizerProject.save_project)
        self.bind("<Control-S>", self.OrganizerProject.save_project)
        # Ctrl+F для перевода фокуса на поле поиска
        self.bind("<Control-f>", lambda event: self.search_entry.focus_set())
        self.bind("<Control-F>", lambda event: self.search_entry.focus_set())

        # Сохранение текущего состояния дерева
        self.tree_structure = {}

