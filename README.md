# Bibauto app
## O que é?

BibAuto é um automatizador de bibliotecas com o sistema Biblivre capaz de cadastrar livros com apenas a foto da página de informações.
## Como rodar:

### uv

Rodar como um app de desktop:

```bash
uv run flet run
```

Rodar na web (AVISO: É provável que o app não funcione via web devido a manipulação de caminhos de arquivos.):

```bash
uv run flet run --web
```

Para mais detalhes sobre rodar o app, vá para [Getting Started Guide](https://docs.flet.dev/).

## Build the app

### Android

```bash
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://docs.flet.dev/publish/android/).

### iOS

```bash
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://docs.flet.dev/publish/ios/).

### macOS

```bash
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://docs.flet.dev/publish/macos/).

### Linux

```bash
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://docs.flet.dev/publish/linux/).

### Windows

```bash
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://docs.flet.dev/publish/windows/).

### Web

```bash
flet build web -v
```

For more details on building Web app, refer to the [Web Packaging Guide](https://docs.flet.dev/publish/web/).