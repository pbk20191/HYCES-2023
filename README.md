# HYCES-2023
HYCES-2023 raspberry pi project
이 프로젝트는 Window, Mac, Linux에서 동작하지만 권장 운영체제는 Mac과 Linux입니다.

프로젝트 세팅 방법
-----
해당 프로젝트는 Python3.11로 VSCode에서 개발하는 것을 기준으로 설명합니다.
VSCode에는 [Python-Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)이 설치가 되어 있어야 합니다.

1. 이 프로젝트를 clone한다

2. VSCode에서 Ctl/Cmd+Shift+P를 누르고 'Python: Create Environment'를 검색
  
3. venv 선택 -> Python3.11 -> requirements.txt를 선택하여 venv를 구성한다

4. 'Run and Debug' 탭에서 Run을 선택하여 실행할 수 있다. Build를 실행시에는 프로젝트를 패키징하여 하나의 실행가능한 파일로 만든다.

----

GPIO 설정 변경하기
------
GPIO제어는 원격제어/로컬제어/Mocking 3가지 환경설정이 존재한다
- 로컬제어모드는 라즈베리파이 내부에서 실행할 때만 가능하다
- 원격제어모드는 원격GPIO가 활성화되어 있고, 원격접속이 가능한 라즈베리파이가 존재할때 사용가능하다
- Mocking은 가짜 GPIO 설정으로 프로그램 실행은 되지만 실제로는 작동하지 않아, 라즈베리파이 없이 desktop에서 사용이 가능하다.

src/main.py 에 아래와 같은 소스코드 중 하나를 가지고 3가지 옵션 하나를 선택할 수 있다.

    # this pin_factory will search for local gpio
    Device.pin_factory = PiGPIOFactory()

    # this pin_factory will use mocking configuration
    Device.pin_factory = MockFactory()

    # this pin_facotry will search for remote GPIO from host:port setup
    Device.pin_factory = PiGPIOFactory(host, port)


Window 주의사항
---------
asyncio lib의 한계점과 winAPI의 특이점으로 인해 stdin 처리 구현에 상당한 차이가 있으며, exit 동작도 상당히 다릅니다.
