import flet as ft
from playwright.async_api import async_playwright, expect
import time
import json

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.title = 'Bib Auto'
    page.scroll = ft.ScrollMode.AUTO
    page.window_icon = "src/assets/icon.png" 

    async def PickPhoto(e: ft.Event[ft.Button]):
        nonlocal PATH
        file = await ft.FilePicker().pick_files(
            allow_multiple=False,
            allowed_extensions=[
                'png',
                'jpeg',
                'jpg',
                'heic'
            ],
        )

        if file:
            PATH = [f.path for f in file]
            PATH = PATH[0]
            
        if PATH:
            image.src = PATH  #type: ignore

    async def SubmitHandler(e):
        nonlocal sended
        if photos.controls == []:
            return
        sended = True
        
        for photograph in photos.controls:
            async with async_playwright() as p:
                user_data_dir = "bot"
                context = await p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=head.value,
                    args=["--disable-blink-features=AutomationControlled"]
                )

                page = context.pages[0]
                await page.goto(ailink.value.strip())

                if prepare:
                    await page.wait_for_timeout(80000)

                await expect(page.locator("[data-test-id='side-nav-menu-button']")).to_be_visible(timeout=60000)

                await page.get_by_role("button", name="Abrir o menu de envio de").click()
                await expect(page.get_by_role("menu", name="Opções de upload do arquivo")).to_be_visible()

                async with page.expect_file_chooser() as fc_info:
                    await page.locator("[data-test-id='local-images-files-uploader-button']").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(photograph.controls[0].src)#type:ignore

                await expect(page.get_by_role("button", name="Prévia")).to_be_visible(timeout=60000)

                respostas_antes = await page.locator('message-content').count()
                await page.get_by_role("textbox", name="Insira um comando para o").get_by_role("paragraph").click()
                await page.get_by_role("textbox", name="Insira um comando para o").fill("Siga os mesmos comandos do último pront")

                await page.get_by_role("button", name="Enviar mensagem").click()

                timeout = 60
                intervalo = 1
                tempo_gasto = 0

                while tempo_gasto < timeout:
                    respostas_agora = await page.locator('message-content').count()
                    if respostas_agora > respostas_antes:
                        print(f"Total: {respostas_agora}")
                        break
                    time.sleep(intervalo)
                    tempo_gasto += intervalo
                else:
                    raise TimeoutError("Cabo o tempo, se lascou XD.")
                copy_locator = page.locator('button[aria-label="Copiar"]').nth(respostas_antes)
                await copy_locator.wait_for(state="visible", timeout=60000)
 
                nova_resposta = page.locator('message-content').nth(respostas_antes)
                INFO = await nova_resposta.inner_text()

                print("Resposta:")
                print(INFO)
 
                INFO = INFO.split("\n") #type: ignore

                await page.goto(biblivrehost.value.strip())
                await page.get_by_role("textbox", name="Usuário").click()
                await page.get_by_role("textbox", name="Usuário").fill("gabriel")
                await page.get_by_role("textbox", name="Senha").click()
                await page.get_by_role("textbox", name="Senha").fill("gabgab")
                await page.get_by_role("button", name="Entrar").click()
                await page.goto(biblivrehost.value.strip())
                await page.get_by_text("Novo registro").click()
                await page.get_by_role("group", name="Título principal(245)[ ? ]").get_by_role("textbox").click()
                await page.get_by_role("group", name="Título principal(245)[ ? ]").get_by_role("textbox").fill(INFO[0])
                await page.get_by_role("group", name="Autor - Nome pessoal(100)[ ? ]").get_by_role("textbox").click()
                await page.get_by_role("group", name="Autor - Nome pessoal(100)[ ? ]").get_by_role("textbox").fill(INFO[1])
                await page.get_by_role("group", name="Assunto - Nome pessoal(600").get_by_role("textbox").click()
                await page.get_by_role("group", name="Assunto - Nome pessoal(600").get_by_role("textbox").fill(INFO[1])
                await page.get_by_role("group", name="ISBN(020)[ ? ]").get_by_role("textbox").click()
                await page.get_by_role("group", name="ISBN(020)[ ? ]").get_by_role("textbox").fill(INFO[2] if INFO[2] != '' else photograph.controls[2].value)#type:ignore
                await page.get_by_role("group", name="Classificação Decimal Universal(080)[ ? ]").get_by_role("textbox").click()
                await page.get_by_role("group", name="Classificação Decimal Universal(080)[ ? ]").get_by_role("textbox").fill(INFO[3])
                await page.get_by_role("group", name="Classificação Decimal Dewey(").get_by_role("textbox").click()
                await page.get_by_role("group", name="Classificação Decimal Dewey(").get_by_role("textbox").fill(INFO[4])
                await page.get_by_role("group", name="Número de chamada - Localiza").locator("input[name=\"a\"]").click()
                await page.get_by_role("group", name="Número de chamada - Localiza").locator("input[name=\"a\"]").fill(INFO[4])
                await page.get_by_role("group", name="Número de chamada - Localiza").locator("input[name=\"b\"]").click()
                await page.get_by_role("group", name="Número de chamada - Localiza").locator("input[name=\"b\"]").fill(INFO[5])
                await page.get_by_role("group", name="Número de chamada - Localiza").locator("input[name=\"c\"]").click()
                await page.get_by_role("group", name="Número de chamada - Localiza").locator("input[name=\"c\"]").fill(INFO[6])
                await page.get_by_role("group", name="Publicação, edição. Etc.(260").locator("input[name=\"a\"]").click()
                await page.get_by_role("group", name="Publicação, edição. Etc.(260").locator("input[name=\"a\"]").fill(INFO[7])
                await page.get_by_role("group", name="Publicação, edição. Etc.(260").locator("input[name=\"b\"]").click()
                await page.get_by_role("group", name="Publicação, edição. Etc.(260").locator("input[name=\"b\"]").fill(INFO[8])
                await page.get_by_role("group", name="Publicação, edição. Etc.(260").locator("input[name=\"c\"]").click()
                await page.get_by_role("group", name="Publicação, edição. Etc.(260").locator("input[name=\"c\"]").fill(INFO[9])
                await page.locator("div:nth-child(9) > .datafield > .subfields > div > .value > .finput").first.click()
                await page.locator("div:nth-child(9) > .datafield > .subfields > div > .value > .finput").first.fill(INFO[10])
                await page.get_by_role("group", name="Descrição física(300)[ ? ]").locator("input[name=\"b\"]").click()
                await page.get_by_role("group", name="Descrição física(300)[ ? ]").locator("input[name=\"b\"]").fill(INFO[11])
                await page.get_by_role("group", name="Descrição física(300)[ ? ]").locator("input[name=\"c\"]").click()
                await page.get_by_role("group", name="Descrição física(300)[ ? ]").locator("input[name=\"c\"]").fill(INFO[12])
                await page.locator("input[name=\"holding_count\"]").click()
                await page.locator("input[name=\"holding_count\"]").fill(photograph.controls[1].value)#type:ignore
                await page.evaluate("CatalogingInput.saveRecord();")
                print('Cadastrado.')
                

    def PackageMix(e): #Não achei outro nome
        if PATH == '':
            return
        photo = ft.Column(
                    controls = [#type: ignore
                        ft.Image(src=PATH, height = 200),#type: ignore
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

    image = ft.Image(src='', height=200)#type: ignore
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
        label='URL para a IA',
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
        disabled=True if sended else False
    )   

    tutorial = '''Primeiramente, pegue uma ia de sua preferência (que tenha suporte para imagens) e coloque esse promt, junto de uma foto da página das informações de um livro de demonstração:

    
Baseando-se na imagem da página do livro, escreva APENAS e UNICAMENTE, sem textos adicionais, as seguintes informações, separadas por paragrafo. A seguir, está a lista das inforações que você deve buscar:

titulo_principal
autor
isbn
cdu
cdd
autor_codigo
edicao
local
editor
ano
paginas
il
dimencoes

Para que não haja confusões: ano é o ano de publicação do livro, il é se o material é ilustrativo. Note que o nome deve estar na seguinte forma: [último sobrenome], [nome completo antes do último sobrenome]. NÃO escreva qual informação é qual, apenas deixe em ordem dos parágrafos. Se tiver edição, apenas escreva seu número SEM pontos (estraga a formatação).
Caso a página não apresente alguma das informações acima, você deve escrever: Não tem


O promt está em um arquivo de texto nos arquivos do app.
É confirmado que funciona no Gemini, mas não em outras ias. Se quiser um porte específico, entre em cotato comigo via GitHub.
Feito isso, vá na área de Configurações, copie e cole a URL da conversa da Ia na caixa: URL para Ia.
Agora, na mesma área, coloque a URL do biblivre na área da Catalogação Bibliográfica, em seguida do seu usuário e senha. Clique em Salvar.
Agora, ligue a opção Prepação, coloque alguma imagem na área de Cadastrar, aperte em Enviar, vá na área Enviar e aperte em Cadastrar, uma janela do chrome deve se abrir.
Nela, dê login com a conta do Google da conversa da ia e saia. Pode desligar a opção Prepação.
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
                                    image,
                                    number_of_copies,
                                    isbn,
                                    button,
                                    submit_button
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
                                    prepare := ft.Switch(label='Preparação')
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

if __name__ == '__main__':
    ft.run(main)
