import flet as ft
from playwright.async_api import async_playwright, expect
import time
import json
import geminiAPI as API

first_opened = True
chat_session = None

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.title = 'Bib Auto'
    page.scroll = ft.ScrollMode.AUTO
    page.window_icon = "src/assets/icon.png" 

    async def PickPhoto(e: ft.Event[ft.Button]):
        nonlocal PATH
        file = await ft.FilePicker().pick_files(
            allow_multiple=True,
            allowed_extensions=[
                'png',
                'jpeg',
                'jpg',
                'heic'
            ],
        )

        if file:
            PATH = [f.path for f in file]
        if PATH:
            for P in PATH:
                images.controls.append(ft.Image(src = P, height=200))

    async def SubmitHandler(e):
        nonlocal sended
        global first_opened
        global chat_session

        if not photos.controls:
            return
        
        if first_opened:
            system_prompt = """Pelas próximas mensagens, você fará o seguinte:
Baseando-se na imagem da página do livro, escreva APENAS e UNICAMENTE, sem textos adicionais, as seguintes informações, separadas por parágrafo. A seguir, está a lista das inforações que você deve buscar:

título_principal
autor
isbn
cdu
cdd
autor_código
edição
local
editor
ano
paginas
il
dimenções
assunto_tópico

Para que não haja confusões: ano é o ano de publicação do livro, il é se o material é ilustrativo. Note que o nome deve estar na seguinte forma: [último sobrenome], [nome completo antes do último sobrenome]. NÃO escreva qual informação é qual, apenas deixe em ordem dos parágrafos. Se tiver edição, apenas escreva seu número SEM pontos (estraga a formatação).
Caso a página não apresente alguma das informações acima, você deve escrever um paragrafo vazio. No fim, escreva: end."""
            chat_session, client = await API.InnitGeminiChat(ailink.value, system_prompt)
            first_opened = False       

        sended = True

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(biblivrehost.value.strip())
            await page.get_by_role("textbox", name="Usuário").fill(user.value)
            await page.get_by_role("textbox", name="Senha").fill(password.value)
            await page.get_by_role("button", name="Entrar").click()

            for photograph in photos.controls: 
                image_path = photograph.controls[0].src

                raw_info = await API.SendImageChat(image_path, "Extraia as informações desta página seguindo exatamente as regras fornecidas.", chat_session, client)
                INFO = raw_info.split("\n")

                while len(INFO) < 14:
                    INFO.append("")

                await page.goto(biblivrehost.value.strip())
                await page.get_by_text("Novo registro").click()
                
                await page.get_by_role("group", name="Título principal(245)[ ? ]").get_by_role("textbox").fill(INFO[0])
                await page.get_by_role("group", name="Autor - Nome pessoal(100)[ ? ]").get_by_role("textbox").fill(INFO[1])
                await page.get_by_role("group", name="Assunto - Nome pessoal(600").get_by_role("textbox").fill(INFO[1])
                
                isbn_value = INFO[2] if INFO[2].strip() and INFO[2] != 'Não tem' else photograph.controls[2].value
                await page.get_by_role("group", name="ISBN(020)[ ? ]").get_by_role("textbox").fill(str(isbn_value))
                
                await page.get_by_role("group", name="Classificação Decimal Universal(080)[ ? ]").get_by_role("textbox").fill(INFO[3])
                await page.get_by_role("group", name="Classificação Decimal Dewey(").get_by_role("textbox").fill(INFO[4])
                
                chamada_group = page.get_by_role("group", name="Número de chamada - Localiza")
                await chamada_group.locator("input[name=\"a\"]").fill(INFO[4])
                await chamada_group.locator("input[name=\"b\"]").fill(INFO[5])
                await chamada_group.locator("input[name=\"c\"]").fill(INFO[6])
                
                pub_group = page.get_by_role("group", name="Publicação, edição. Etc.(260")
                await pub_group.locator("input[name=\"a\"]").fill(INFO[7])
                await pub_group.locator("input[name=\"b\"]").fill(INFO[8])
                await pub_group.locator("input[name=\"c\"]").fill(INFO[9])
                
                await page.locator("div:nth-child(9) > .datafield > .subfields > div > .value > .finput").first.fill(INFO[10])
                
                desc_fisica = page.get_by_role("group", name="Descrição física(300)[ ? ]")
                await desc_fisica.locator("input[name=\"b\"]").fill(INFO[11])
                await desc_fisica.locator("input[name=\"c\"]").fill(INFO[12])
                
                await page.locator("fieldset:nth-child(10) > .subfields > .subfield > .value > .finput").fill(INFO[13])
                await page.locator("input[name=\"holding_count\"]").fill(str(photograph.controls[1].value))
                
                await page.evaluate("CatalogingInput.saveRecord();")
                print(f'Livro "{INFO[0]}" cadastrado.')

            await browser.close()

        sended = False
        photos.controls.clear()
                

    def PackageMix(e): #Não achei outro nome
        if not images.controls:
            return
        for PATHes in images.controls:
            photo = ft.Column(
                        controls = [#type: ignore
                            ft.Image(src=PATHes.src, height = 200),#type: ignore
                            ft.Text(number_of_copies.value.strip()),
                            ft.Text(isbn.value.strip()),
                            ft.IconButton(ft.Icons.DELETE, icon_color = 'red', on_click=  lambda _: DeletePackage(photo)),
                            ft.Divider(),
                        ]
                    )
            photos.controls.append(
                photo
            )
    
    def DeletePackage(e): 
        photos.controls.remove(e)

    def Save(e):
        config = {
            "config": [
                ailink.value.strip(),
                biblivrehost.value.strip(),
                user.value.strip(),
                password.value.strip(),
                head.value
            ]
        }

        with open("src/configs.json", "w") as f:
            json.dump(config, f, indent=4)

    with open("src/configs.json", "r") as f:
        configuracoes = json.load(f)

    sended = False

    PATH = ''
 
    photos = ft.Column()

    images = ft.Column(
        controls=[

        ]
    )
    number_of_copies = ft.TextField(
        label='Número de exemplares',
        value = '1',
        keyboard_type = ft.KeyboardType.NUMBER,
        width=200
    )
    isbn = ft.TextField(
        label='ISBN (caso não houver na página)'
    )
    button = ft.Button(
        "Selecionar Foto do Livro",
        icon=ft.Icons.IMAGE,
        on_click=PickPhoto
    )
    submit_button = ft.Button(
        content='Mandar', icon=ft.Icons.SEND, on_click= PackageMix
    )
    ailink = ft.TextField(
        label='Chave API do Google Gemini',
        expand=True,
        value=configuracoes['config'][0]
    )
    biblivrehost = ft.TextField(
        label = 'Link do biblivre',
        expand=True,
        value=configuracoes['config'][1]
    )
    user = ft.TextField(
        label='Usuário do biblivre',
        value = configuracoes['config'][2]
    )
    password = ft.TextField(
        label='Senha do biblivre',
        value=configuracoes['config'][3] 
    )
    cadastrar = ft.Button(
        'Cadastrar',
        bgcolor='green',
        color = 'white',
        on_click = SubmitHandler,
        disabled=False if not sended else True
    )   

    tutorial = '''Primeiramente, consiga uma chave API do gemini no site ai.dev
Feito isso, vá na área de Configurações, copie e cole o código da chave na caixa Chave API do Google Gemini.
Agora, na mesma área, coloque a URL do biblivre na área da Catalogação Bibliográfica, em seguida do seu usuário e senha. Clique em Salvar.
Esses são os passos necessários para começar a automação. Note que essas informações são salvas localmente.


Para cadastrar, vá na área Cadastrar e coloque a foto da página de informações do livro. Note que o programa não salva exemplares repetidos, então sempre busque pelo nome do livro e registre um novo exemplar caso tenha um já existente.
Coloque a quantiedade de exemplares e o ISBN (caso não tenha na página do livro) em suas devidas caixas. Clique em Mandar. Repita esse processo por quantos livros quizer.
É recomendado NÃO colocar muitos exemplares na lista de Mandar, para evitar quaisquer problema.
Quando satisfeito, vá na área Mandar e clique em Cadastrar. Aguarde o processo finalizar e os livros deverão estar cadastrados no Biblivre.
'''

    tabas = ft.Tabs(
        length=4,
        content=ft.Column(
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label='Cadastrar'),
                        ft.Tab(label='Mandar'),
                        ft.Tab(label='Configurações'),
                        ft.Tab(label='Como usar'),
                        ],
                    ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    number_of_copies,
                                    isbn,
                                    button,
                                    submit_button,
                                    images,
                                ]
                            )
                        ),
                        ft.Container(
                            content= ft.Column(
                                controls=[
                                    cadastrar,
                                    photos,
                                ]
                            )
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ailink,
                                    biblivrehost,
                                    user,
                                    password,
                                    ft.Button('Salvar', on_click = Save),
                                    head := ft.Switch(label='Abrir browser quando rodar', value = configuracoes['config'][4]),
                                ]
                            ), 
                        ),
                        ft.Container(
                            content = ft.Column(
                                controls = [
                                    ft.Text(tutorial)
                                ]
                            )
                        )
                    ]
                )
            ]
        )
    )


    page.add(
        ft.SafeArea(
            expand = True,
            content=ft.Column(
                [tabas], 
            ),
        )
    )


ft.run(main)