import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Gestore Corsi - Edizione 2026"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None

        # Definiamo il costruttore per tutte le cose dell'interfaccia (non è obbligatorio)

        self.ddPD = None # Menu a tendina, inizializzato a none, poi vediamo
        self.ddCodins = None # Drop down codice insegnamento
        self.btnPrintCorsiPD = None
        self.btnPrintIscrittiCorsiPD = None
        self.btnPrintIscrittiCodins = None
        self.btnPrintCDSCodins = None


    def load_interface(self):
        # title
        self._title = ft.Text("Gestore Corsi - Edizione 2026", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW1
        self.ddPD = ft.Dropdown(label="Periodo Didattico",
                                options = [ft.dropdown.Option("I"), ft.dropdown.Option("II")], # L eopzioni del dropdown è una lista di opzioni
                                width=200)
                                # Dropdown è una parola chiave (anche dropdow.Option (sarebbero le opzioni della tendina)

        self.btnPrintCorsiPD = ft.ElevatedButton(text="Stampa Corsi", #Testo del pulsante
                                                 on_click=self._controller.handlePrintCorsiPD,
                                                 width=300)
        self.btnPrintIscrittiCorsiPD = ft.ElevatedButton(text="Stampa numero iscritto",
                                                 on_click=self._controller.handlePrintIscrittiCorsiPD, # on_click è il metodo del bottone, si scrive sul controller
                                                 width=300)

        row1 = ft.Row([self.ddPD, self.btnPrintCorsiPD, self.btnPrintIscrittiCorsiPD], alignment=ft.MainAxisAlignment.CENTER)

        # ROW 2

        self.ddCodins = ft.Dropdown(label = "Corso", width=200) # Non sappiamo ancora le opzioni perche sono contenute sul database
        self._controller.fillddCodins() # Una volta creato il dropdown posso chiedere al controlelr di riempirlo

        self.btnPrintIscrittiCodins = ft.ElevatedButton(text = "Stampa iscritti al corso",
                                                        on_click = self._controller.handlePrintIscrittiCodins,
                                                 width=300) # width è quanto sono lunghi i pulsanti
        self.btnPrintCDSCodins = ft.ElevatedButton(text = "Stampa CDS afferenti",
                                                   on_click = self._controller.handlePrintCDSCodins,
                                                 width=300)

        row2 = ft.Row([self.ddCodins, self.btnPrintIscrittiCodins, self.btnPrintCDSCodins], alignment=ft.MainAxisAlignment.CENTER)
        self._page.add(row1, row2)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
