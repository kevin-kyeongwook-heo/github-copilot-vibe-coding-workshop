# GitHub Copilot Vibe 코딩 워크샵

![GitHub Copilot Vibe 코딩 워크샵](../../images/banner.png)

Python, JavaScript, Java, .NET 등 다양한 프로그래밍 언어에서 [GitHub Copilot](https://docs.github.com/copilot/about-github-copilot/what-is-github-copilot)과 최신 기능들로 바이브 코딩을 하고, 컨테이너화를 통해 앱을 클라우드 네이티브로 만들어 보세요. 뛰어들 준비가 되셨나요?

## 배경

Contoso는 다양한 야외 활동 제품을 판매하는 회사입니다. Contoso의 마케팅 부서는 기존 고객과 잠재 고객에게 제품을 홍보하기 위한 마이크로 소셜 미디어 웹사이트를 런칭하고자 합니다. 첫 번째 MVP로서, 웹사이트를 빠르게 구축하고자 합니다. Contoso의 IT 부서에는 현재 각각 Python과 JavaScript를 사용하는 두 명의 개발자가 있습니다. 출시일이 빠르게 다가오고 있어서, 두 개발자 모두 애플리케이션을 빠르게 개발해야 합니다.

하지만 상황은 다음과 같습니다...

## 워크샵 목표

- GitHub Copilot 에이전트 모드를 사용하여 애플리케이션 구축하기.
- GitHub Copilot에 커스텀 지시사항을 추가하여 GitHub Copilot을 더 잘 제어하기.
- GitHub Copilot에 다양한 MCP 서버를 추가하여 애플리케이션을 더 정확하게 구축하기.

## 다양한 언어로 제공되는 워크샵

이 워크샵 자료는 현재 다음 언어로 제공됩니다:

[English](../../README.md) | [Español](../es-es/) | [Français](../fr-fr/) | [日本語](../ja-jp/) | [한국어](./README.md) | [Português](../pt-br/) | [中文(简体)](../zh-cn/)

## 전제 조건

이 워크샵에서는 웹 브라우저 외에 별도의 준비가 필요 없기 때문에 [GitHub Codespaces](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces)를 적극 권장합니다.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/kevin-kyeongwook-heo/github-copilot-vibe-coding-workshop)

하지만 정말로 본인의 머신을 사용해야 한다면, 아래에서 확인된 모든 것들을 설치했는지 확인하세요.

### 공통

- [Visual Studio Code](https://code.visualstudio.com/)
- VS Code [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) 확장
- VS Code [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) 확장
- 💥 Windows 사용자용 👉 [PowerShell 7](https://learn.microsoft.com/powershell/scripting/install/installing-powershell)
- [git CLI](https://git-scm.com/downloads)
- [GitHub CLI](https://cli.github.com/)
- [Docker Desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)

### Python

- [pyenv](https://github.com/pyenv/pyenv) 또는 [pyenv for Windows](https://github.com/pyenv-win/pyenv-win)
- pyenv를 통한 Python 3.12+
- `uv` 패키지 관리자 (권장) 또는 `pip`
- VS Code [Python](https://marketplace.visualstudio.com/items/?itemName=ms-python.python) 확장
- VS Code [Pylance](https://marketplace.visualstudio.com/items/?itemName=ms-python.vscode-pylance) 확장
- VS Code [Python Debugger](https://marketplace.visualstudio.com/items/?itemName=ms-python.debugpy) 확장
- VS Code [autopep8](https://marketplace.visualstudio.com/items/?itemName=ms-python.autopep8) 확장

### JavaScript

- [nvm](https://github.com/nvm-sh/nvm) 또는 [nvm for Windows](https://github.com/coreybutler/nvm-windows)
- nvm을 통한 최신 LTS [Node.js](https://nodejs.org/)

### Java

- [SDKMAN](https://sdkman.io/)
- SDKMAN을 통한 [OpenJDK 21](https://learn.microsoft.com/java/openjdk/download)
- SDKMAN을 통한 [Apache Maven](https://maven.apache.org/download.cgi)
- SDKMAN을 통한 [Gradle Build Tool](https://docs.gradle.org/current/userguide/installation.html)
- SDKMAN을 통한 [Spring Boot Initializr](https://docs.spring.io/spring-boot/cli/installation.html)
- VS Code [Extension Pack for Java](https://marketplace.visualstudio.com/items/?itemName=vscjava.vscode-java-pack) 확장
- VS Code [Spring Boot Extension Pack](https://marketplace.visualstudio.com/items/?itemName=vmware.vscode-boot-dev-pack) 확장

### .NET

- [.NET SDK 9](https://dotnet.microsoft.com/download/dotnet/9.0)
- [VS Code C# Dev Kit](https://marketplace.visualstudio.com/items/?itemName=ms-dotnettools.csdevkit) 확장

## 제품 요구사항 문서

먼저 시작할 곳은 이 [PRD (제품 요구사항 문서)](./product-requirements.md)입니다. 이 문서는 무엇을 해야 하고 어떻게 해야 하는지에 대한 더 나은 이해를 제공할 것입니다.

## 워크샵 지침

아래 링크를 따라 진행하는 자기 주도 워크샵입니다:

| 단계                               | 링크                                                    |
|------------------------------------|---------------------------------------------------------|
| 00: 개발 환경                      | [00-setup.md](./docs/00-setup.md)                       |
| 01: Python 백엔드                 | [01-python.md](./docs/01-python.md)                     |
| 02: JavaScript 프론트엔드          | [02-javascript.md](./docs/02-javascript.md)             |
| 03: Python에서 Java로 마이그레이션 | [03-java.md](./docs/03-java.md)                         |
| 04: JavaScript에서 .NET으로 마이그레이션 | [04-dotnet.md](./docs/04-dotnet.md)                     |
| 05: 컨테이너화                     | [05-containerization.md](./docs/05-containerization.md) |

## 완성된 샘플

각 애플리케이션의 완성된 예제를 확인해보세요. 이들도 GitHub Copilot으로 바이브 코딩되었기 때문에 완벽하지 않을 수 있으며, 앱을 따라할 필요는 없습니다.

| 언어                | 애플리케이션 | 위치                                 |
|---------------------|-------------|--------------------------------------|
| Python 백엔드       | FastAPI     | [python](./complete/python/)         |
| JavaScript 프론트엔드 | React       | [javascript](./complete/javascript/) |
| Java 백엔드         | Spring Boot | [java](./complete/java/)             |
| .NET 프론트엔드     | Blazor      | [dotnet](./complete/dotnet/)         |
| 컨테이너화          | Container   | [containerization](./complete/)      |

## 더 읽어보기...

- [GitHub Codespaces](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces)
- [GitHub Copilot](https://docs.github.com/en/copilot/about-github-copilot/what-is-github-copilot)
- [GitHub Copilot: Agent Mode](https://code.visualstudio.com/blogs/2025/04/07/agentMode)
- [GitHub Copilot: MCP](https://code.visualstudio.com/blogs/2025/05/12/agent-mode-meets-mcp)
- [GitHub Copilot: Custom Instructions](https://code.visualstudio.com/docs/copilot/copilot-customization)
- [GitHub Copilot: Changing AI Models](https://docs.github.com/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat?tool=vscode)
- [Curated MCP Servers](https://github.com/modelcontextprotocol/servers)

---

**면책조항**: 이 문서는 [GitHub Copilot](https://docs.github.com/copilot/about-github-copilot/what-is-github-copilot)에 의해 현지화되었습니다. 따라서 실수가 포함될 수 있습니다. 부적절하거나 잘못된 번역을 발견하면 [issue](https://github.com/microsoft/github-copilot-vibe-coding-workshop/issues/new)를 생성해 주세요.
