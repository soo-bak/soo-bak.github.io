---
layout: single
title: "Unity 에셋 시스템 (3) - Scene Management - soo:bak"
date: "2026-03-05 23:09:00 +0900"
description: 씬 구조, 동기·비동기 씬 로딩, Additive 씬, DontDestroyOnLoad, 씬 언로딩과 메모리 해제를 설명합니다.
tags:
  - Unity
  - 에셋
  - Scene
  - 씬관리
  - 모바일
---

## 에셋이 모여 이루는 가장 큰 단위

[Part 2](/dev/unity/UnityAsset-2/)에서 에셋이 직렬화되어 디스크에 저장되고, 역직렬화되어 메모리에 올라가는 과정을 다루었습니다. Instantiate가 오브젝트를 복제할 때 공유 에셋은 참조만 복사한다는 점, Resources 폴더의 한계도 확인했습니다.

<br>

이 글에서는 에셋들이 모여 구성하는 가장 큰 단위인 **씬(Scene)**의 관리 방법을 살펴봅니다. 로딩과 언로딩을 통해 게임의 흐름(메뉴 → 게임 플레이 → 결과 화면)을 제어하는 기본 메커니즘이며, 전환 시점마다 대규모 메모리 할당과 해제가 발생합니다. 한 번의 전환에 수십~수백 MB의 에셋이 해제되고 다시 로드되므로, 씬 관리 전략은 곧 메모리 관리의 핵심 축이 됩니다.

---

## 씬(Scene)의 구조

씬은 **GameObject들의 집합**입니다. 카메라, 조명, 캐릭터, 배경, UI 등 게임 화면을 구성하는 모든 오브젝트가 하나의 씬에 포함됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 전체 씬 컨테이너 -->
  <rect x="10" y="10" width="500" height="500" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 (.unity 파일)</text>

  <!-- Main Camera -->
  <rect x="30" y="52" width="460" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="72" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Main Camera (GameObject)</text>
  <text x="56" y="90" font-family="sans-serif" font-size="11" fill="currentColor">Transform</text>
  <text x="56" y="106" font-family="sans-serif" font-size="11" fill="currentColor">Camera</text>
  <text x="56" y="118" font-family="sans-serif" font-size="11" fill="currentColor">AudioListener</text>

  <!-- Directional Light -->
  <rect x="30" y="134" width="460" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="154" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Directional Light (GameObject)</text>
  <text x="56" y="172" font-family="sans-serif" font-size="11" fill="currentColor">Transform</text>
  <text x="56" y="184" font-family="sans-serif" font-size="11" fill="currentColor">Light</text>

  <!-- Player -->
  <rect x="30" y="200" width="460" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="220" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Player (GameObject)</text>
  <text x="56" y="238" font-family="sans-serif" font-size="11" fill="currentColor">Transform</text>
  <text x="56" y="254" font-family="sans-serif" font-size="11" fill="currentColor">MeshRenderer</text>
  <!-- 참조 화살표: MeshRenderer → Material → Texture -->
  <line x1="144" y1="251" x2="164" y2="251" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="164,248 170,251 164,254" fill="currentColor"/>
  <text x="174" y="254" font-family="sans-serif" font-size="11" fill="currentColor">Material</text>
  <line x1="222" y1="251" x2="242" y2="251" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="242,248 248,251 242,254" fill="currentColor"/>
  <text x="252" y="254" font-family="sans-serif" font-size="11" fill="currentColor">Texture</text>
  <text x="56" y="270" font-family="sans-serif" font-size="11" fill="currentColor">Rigidbody</text>
  <text x="56" y="284" font-family="sans-serif" font-size="11" fill="currentColor">PlayerController (스크립트)</text>

  <!-- Environment -->
  <rect x="30" y="300" width="460" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="320" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Environment (GameObject)</text>
  <text x="56" y="338" font-family="sans-serif" font-size="11" fill="currentColor">Ground</text>
  <text x="56" y="354" font-family="sans-serif" font-size="11" fill="currentColor">Building_01</text>
  <text x="56" y="366" font-family="sans-serif" font-size="11" fill="currentColor">Building_02</text>

  <!-- Canvas (UI) -->
  <rect x="30" y="382" width="460" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="402" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Canvas (UI)</text>
  <text x="56" y="420" font-family="sans-serif" font-size="11" fill="currentColor">HealthBar</text>
  <text x="56" y="432" font-family="sans-serif" font-size="11" fill="currentColor">ScoreText</text>

  <!-- 보조 설명 -->
  <text x="260" y="468" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">각 GameObject 안에 컴포넌트들이 포함됨</text>
  <text x="260" y="484" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">MeshRenderer → Material → Texture 는 에셋 참조 관계</text>
</svg>
</div>

[Part 2](/dev/unity/UnityAsset-2/)에서 다루었듯이, 씬 파일(`.unity`)은 YAML 형식으로 저장됩니다. 씬에 포함된 모든 GameObject와 컴포넌트가 직렬화되어 기록되고, 각 오브젝트는 fileID로 식별됩니다. 에디터에서 씬을 저장하면 이 YAML 데이터가 디스크에 기록되고, 씬을 로드하면 역직렬화를 통해 메모리에 오브젝트를 복원합니다.

### Build Settings에 씬 등록

빌드에 포함할 씬은 **Build Settings**(File → Build Settings)의 **Scenes In Build** 목록에 등록해야 합니다. 등록된 씬은 인덱스 번호를 부여받으며, 인덱스 0번 씬이 앱 실행 시 가장 먼저 로드되는 씬입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 외곽 컨테이너 -->
  <rect x="10" y="10" width="500" height="260" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Build Settings의 씬 목록</text>

  <!-- Scenes In Build 라벨 -->
  <text x="30" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Scenes In Build:</text>

  <!-- 테이블 외곽 -->
  <rect x="30" y="68" width="340" height="120" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
  <!-- 인덱스 칼럼 구분선 -->
  <line x1="72" y1="68" x2="72" y2="188" stroke="currentColor" stroke-width="1"/>
  <!-- 행 구분선 -->
  <line x1="30" y1="98" x2="370" y2="98" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="30" y1="128" x2="370" y2="128" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="30" y1="158" x2="370" y2="158" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Row 0 (하이라이트) -->
  <rect x="31" y="69" width="338" height="29" fill="currentColor" fill-opacity="0.06"/>
  <text x="51" y="88" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="currentColor">0</text>
  <text x="82" y="88" font-family="monospace" font-size="11" fill="currentColor">Scenes/Loading.unity</text>
  <text x="380" y="88" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">← 앱 시작 시 로드</text>

  <!-- Row 1 -->
  <text x="51" y="118" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">1</text>
  <text x="82" y="118" font-family="monospace" font-size="11" fill="currentColor">Scenes/MainMenu.unity</text>

  <!-- Row 2 -->
  <text x="51" y="148" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">2</text>
  <text x="82" y="148" font-family="monospace" font-size="11" fill="currentColor">Scenes/GamePlay.unity</text>

  <!-- Row 3 -->
  <text x="51" y="178" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">3</text>
  <text x="82" y="178" font-family="monospace" font-size="11" fill="currentColor">Scenes/Result.unity</text>

  <!-- 결론 라인 -->
  <text x="30" y="216" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">→ 인덱스 0번이 첫 실행 씬</text>
  <text x="30" y="234" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">→ 목록에 없는 씬은 빌드에 포함되지 않음</text>
  <text x="30" y="252" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">→ 씬 이름 또는 인덱스로 런타임 로딩 가능</text>
</svg>
</div>

<br>

Unity의 **Addressables** 시스템을 사용하면 Build Settings에 등록하지 않은 씬도 런타임에 로드할 수 있지만, `SceneManager`를 통한 기본적인 씬 전환에는 Build Settings 등록이 필요합니다.

---

## SceneManager.LoadScene — 동기 로딩

`SceneManager.LoadScene`은 씬을 **동기적(Synchronous)**으로 로드합니다. 호출 자체는 즉시 반환되어 같은 프레임 내 나머지 코드가 계속 실행되지만, 실제 씬 로딩은 다음 프레임에서 수행됩니다. 로딩이 완료될 때까지 메인 스레드가 블로킹되는데, Unity는 게임 로직, 렌더링 명령 생성, 입력 처리를 모두 메인 스레드에서 순차 실행하므로 블로킹 동안 화면 갱신과 입력 처리가 멈춥니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 540" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 제목 -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">동기 로딩의 실행 흐름</text>

  <!-- 프레임 N 영역 -->
  <rect x="10" y="36" width="540" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="24" y="56" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프레임 N</text>

  <!-- 호출 시점 -->
  <rect x="30" y="66" width="500" height="54" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">호출 시점</text>
  <text x="44" y="100" font-family="sans-serif" font-size="11" fill="currentColor">SceneManager.LoadScene("GamePlay") 호출</text>
  <text x="44" y="114" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">호출 이후 같은 프레임 내 나머지 코드는 계속 실행됨</text>

  <!-- 세로 화살표: 프레임 N → 다음 프레임 블로킹 -->
  <line x1="280" y1="126" x2="280" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="277,140 280,147 283,140" fill="currentColor"/>

  <!-- 다음 프레임 (블로킹 구간) -->
  <rect x="30" y="150" width="500" height="254" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="44" y="170" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">다음 프레임 (메인 스레드 블로킹 — 로딩 완료까지)</text>

  <!-- 6단계 -->
  <rect x="50" y="182" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="200" font-family="sans-serif" font-size="11" fill="currentColor">1. 현재 씬의 모든 오브젝트 파괴 (OnDisable → OnDestroy)</text>

  <line x1="280" y1="210" x2="280" y2="218" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,218 280,222 282,218" fill="currentColor"/>

  <rect x="50" y="224" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="242" font-family="sans-serif" font-size="11" fill="currentColor">2. 새 씬 파일 읽기 (디스크 I/O)</text>

  <line x1="280" y1="252" x2="280" y2="260" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,260 280,264 282,260" fill="currentColor"/>

  <rect x="50" y="266" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="284" font-family="sans-serif" font-size="11" fill="currentColor">3. 참조 에셋 로딩 (텍스처, 메쉬, 오디오 등)</text>

  <line x1="280" y1="294" x2="280" y2="302" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,302 280,306 282,302" fill="currentColor"/>

  <rect x="50" y="308" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="326" font-family="sans-serif" font-size="11" fill="currentColor">4. 모든 오브젝트 역직렬화 (메모리 배치)</text>

  <line x1="280" y1="336" x2="280" y2="344" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,344 280,348 282,344" fill="currentColor"/>

  <rect x="50" y="350" width="220" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="368" font-family="sans-serif" font-size="11" fill="currentColor">5. Awake() 호출</text>

  <rect x="290" y="350" width="220" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="304" y="368" font-family="sans-serif" font-size="11" fill="currentColor">6. OnEnable() 호출</text>

  <text x="530" y="400" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">화면 갱신 없음 (게임 멈춤)</text>

  <!-- 세로 화살표: 프레임 N → N+1 -->
  <line x1="280" y1="416" x2="280" y2="432" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="277,432 280,439 283,432" fill="currentColor"/>

  <!-- 로딩 완료 후 첫 프레임 -->
  <rect x="10" y="442" width="540" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="24" y="462" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">로딩 완료 후 첫 프레임</text>
  <text x="44" y="480" font-family="sans-serif" font-size="11" fill="currentColor">Start() 호출 (첫 Update() 직전)</text>
  <text x="44" y="494" font-family="sans-serif" font-size="11" fill="currentColor">새 씬의 첫 Update() 실행</text>

  <!-- 보조 텍스트 -->
  <text x="280" y="524" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">실제 씬 전환은 다음 프레임에서 수행 · 로딩 완료까지 메인 스레드 블로킹 · 화면 갱신 없음</text>
</svg>
</div>

동기 로딩의 가장 큰 문제는 **프레임 정지**입니다. 씬의 에셋 총량이 클수록, 참조하는 에셋이 많을수록 정지 시간이 길어집니다. 에셋이 많은 게임 씬을 동기 로딩하면 2~5초 이상 화면이 멈출 수 있습니다. 사용자에게는 앱이 멈춘 것처럼 보이며, 모바일 OS가 응답 없음으로 판단하여 앱을 강제 종료하는 경우도 발생합니다.

동기 로딩이 적합한 경우는 제한적입니다. 앱 시작 시 첫 번째 씬을 로드하는 경우(어차피 스플래시 화면이 표시됨), 또는 에셋이 거의 없는 작은 씬을 로드하는 경우에만 사용합니다.

### 기존 씬의 처리

기본 동작(LoadSceneMode.Single)에서는 새 씬을 로드하기 전에 현재 씬의 모든 오브젝트를 파괴합니다. 각 오브젝트의 OnDisable, OnDestroy 순서로 콜백이 호출됩니다. 새 씬 로드가 완료되면 Unity가 자동으로 `Resources.UnloadUnusedAssets()`를 호출하여, 이전 씬의 오브젝트만 참조하던 에셋을 메모리에서 해제합니다. 다만 이 자동 해제는 새 씬의 에셋 로딩이 끝난 뒤에 수행되므로, 전환 중에는 이전 씬과 새 씬의 에셋이 동시에 메모리에 올라가는 피크 구간이 생길 수 있습니다.

---

## SceneManager.LoadSceneAsync — 비동기 로딩

`SceneManager.LoadSceneAsync`는 씬을 **비동기적(Asynchronous)**으로 로드하여 동기 로딩의 프레임 정지 문제를 해결합니다. 파일 읽기(I/O)와 역직렬화의 상당 부분은 백그라운드 스레드에서 수행되고, 로드된 오브젝트를 씬에 통합(Integration)하는 작업은 메인 스레드에서 여러 프레임에 걸쳐 분산 처리됩니다. 따라서 로딩이 진행되는 동안에도 게임이 계속 실행됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">비동기 로딩의 실행 흐름</text>
  <line x1="90" y1="58" x2="590" y2="58" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="590,55 597,58 590,61" fill="currentColor"/>
  <text x="604" y="62" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">시간</text>
  <text x="110" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">N</text>
  <line x1="110" y1="54" x2="110" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="190" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+1</text>
  <line x1="190" y1="54" x2="190" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+2</text>
  <line x1="270" y1="54" x2="270" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="350" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+3</text>
  <line x1="350" y1="54" x2="350" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="440" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+K</text>
  <line x1="440" y1="54" x2="440" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="540" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">N+K+1</text>
  <line x1="540" y1="54" x2="540" y2="62" stroke="currentColor" stroke-width="1"/>
  <line x1="390" y1="70" x2="390" y2="310" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity="0.3"/>
  <text x="14" y="108" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">백그라운드</text>
  <text x="14" y="120" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">스레드</text>
  <rect x="90" y="80" width="370" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">파일 I/O + 역직렬화</text>
  <text x="275" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">디스크 읽기, 에셋 데이터 역직렬화</text>
  <text x="14" y="170" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">메인</text>
  <text x="14" y="182" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">스레드</text>
  <rect x="90" y="148" width="370" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">게임 실행 + 오브젝트 통합 처리</text>
  <text x="275" y="184" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">화면 갱신 유지, 매 프레임 분산 처리</text>
  <rect x="480" y="80" width="120" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="540" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 활성화</text>
  <text x="540" y="120" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Awake()</text>
  <text x="540" y="138" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">OnEnable()</text>
  <text x="540" y="156" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Start()</text>
  <text x="540" y="176" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">progress: 1.0</text>
  <line x1="460" y1="106" x2="476" y2="106" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="476,103 482,106 476,109" fill="currentColor"/>
  <line x1="460" y1="174" x2="476" y2="174" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="476,171 482,174 476,177" fill="currentColor"/>
  <text x="44" y="240" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">progress</text>
  <rect x="90" y="224" width="510" height="28" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <rect x="90" y="224" width="370" height="28" rx="5" fill="currentColor" fill-opacity="0.08"/>
  <text x="110" y="242" font-family="sans-serif" font-size="10" fill="currentColor">0.0</text>
  <text x="190" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">0.1</text>
  <text x="270" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">0.3</text>
  <text x="350" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">0.5</text>
  <text x="440" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">0.9</text>
  <text x="540" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">1.0</text>
  <line x1="460" y1="224" x2="460" y2="252" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2"/>
  <rect x="90" y="272" width="370" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="275" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">에셋 로딩 구간 (0.0 ~ 0.9)</text>
  <rect x="480" y="272" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="540" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">활성화 (0.9 ~ 1.0)</text>
  <text x="310" y="326" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">백그라운드 스레드: I/O와 역직렬화 담당</text>
  <text x="310" y="342" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">메인 스레드: 게임 실행 유지 + 오브젝트 통합 담당</text>
  <text x="310" y="358" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">로딩 중에도 화면 갱신과 입력 처리가 계속됨</text>
</svg>
</div>

### AsyncOperation과 progress

`LoadSceneAsync`는 로딩 상태를 추적할 수 있는 **AsyncOperation** 객체를 반환합니다. `progress` 프로퍼티의 값은 0에서 1까지 변화하지만, 실제 로딩 작업은 0~0.9 구간에서 수행됩니다. 0.9에서 1.0으로의 전환은 씬 활성화(오브젝트 초기화) 단계에 해당합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">progress 값의 의미</text>
  <!-- 진행 바 전체 -->
  <rect x="30" y="38" width="480" height="50" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <!-- 에셋 로딩 구간 (0.0 ~ 0.9) -->
  <rect x="30" y="38" width="384" height="50" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="222" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">에셋 로딩 구간</text>
  <text x="222" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">디스크 읽기 · 역직렬화 · 메모리 배치</text>
  <!-- 활성화 구간 (0.9 ~ 1.0) -->
  <rect x="414" y="38" width="96" height="50" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="462" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활성화</text>
  <text x="462" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Awake · Start</text>
  <!-- 눈금 레이블 -->
  <text x="30" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">0.0</text>
  <line x1="30" y1="88" x2="30" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <text x="414" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">0.9</text>
  <line x1="414" y1="88" x2="414" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <text x="510" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1.0</text>
  <line x1="510" y1="88" x2="510" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <!-- 구분선 0.9 -->
  <line x1="414" y1="38" x2="414" y2="88" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2"/>
  <!-- 하단: 로딩 바 환산 공식 -->
  <rect x="100" y="128" width="340" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">로딩 바 표시 비율 = operation.progress / 0.9f</text>
  <text x="270" y="160" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">0.9 이전까지를 100%로 환산</text>
  <!-- 화살표: 0.0~0.9 구간 → 공식 -->
  <line x1="222" y1="88" x2="222" y2="124" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <polygon points="219,124 222,130 225,124" fill="currentColor"/>
  <!-- 보조 설명 -->
  <text x="270" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">progress가 0.9에 도달하면 에셋 로딩 완료, 이후 씬 활성화 단계 진입</text>
</svg>
</div>

### allowSceneActivation으로 활성화 시점 제어

`AsyncOperation.allowSceneActivation`을 `false`로 설정하면, `progress`가 0.9에 도달해도 씬이 활성화되지 않고 대기합니다. 데이터 로딩이 끝난 뒤 원하는 시점(사용자 입력, 애니메이션 종료 등)에 `allowSceneActivation = true`로 설정하면 씬이 활성화됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 390" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 외곽 컨테이너 -->
  <rect x="10" y="10" width="500" height="370" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">allowSceneActivation 활용</text>

  <!-- Phase 1: 로딩 시작 -->
  <rect x="30" y="48" width="460" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="66" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1. 로딩 시작</text>
  <text x="44" y="82" font-family="monospace" font-size="10" fill="currentColor">AsyncOperation op = SceneManager.LoadSceneAsync("GamePlay");</text>
  <text x="44" y="96" font-family="monospace" font-size="10" fill="currentColor">op.allowSceneActivation = false;</text>

  <!-- 화살표 1→2 -->
  <line x1="260" y1="106" x2="260" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="257,120 260,127 263,120" fill="currentColor"/>

  <!-- Phase 2: 대기 (점선) -->
  <rect x="30" y="130" width="460" height="58" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="44" y="148" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2. 로딩 진행 (progress → 0.9)</text>
  <text x="44" y="166" font-family="sans-serif" font-size="11" fill="currentColor">씬 데이터는 메모리에 준비 완료</text>
  <text x="44" y="180" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">활성화되지 않음 — 대기 상태</text>

  <!-- 화살표 2→3 -->
  <line x1="260" y1="188" x2="260" y2="202" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="257,202 260,209 263,202" fill="currentColor"/>

  <!-- Phase 3: 활성화 -->
  <rect x="30" y="212" width="460" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="230" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3. 원하는 시점에 활성화</text>
  <text x="44" y="246" font-family="monospace" font-size="10" fill="currentColor">op.allowSceneActivation = true;</text>
  <text x="44" y="262" font-family="sans-serif" font-size="11" fill="currentColor">→ Awake, OnEnable, Start 호출</text>
  <text x="44" y="276" font-family="sans-serif" font-size="11" fill="currentColor">→ 씬 전환 완료</text>

  <!-- 활용 예 -->
  <line x1="30" y1="300" x2="490" y2="300" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text x="30" y="320" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활용 예:</text>
  <text x="44" y="338" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">• 로딩 화면의 "터치하여 시작" 연출</text>
  <text x="44" y="354" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">• 최소 로딩 시간 보장 (너무 빠르면 로딩 화면이 깜빡임)</text>
  <text x="44" y="370" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">• 다른 비동기 작업(네트워크 등)과 동기화</text>
</svg>
</div>

<br>

`allowSceneActivation`이 `false`인 동안에는 `AsyncOperation.isDone`도 `true`가 되지 않습니다. 로딩 완료를 `isDone`으로 검사하는 코드(예: 코루틴의 `yield return operation`)는 `allowSceneActivation`이 `true`로 전환될 때까지 완료되지 않습니다. 로딩 완료 여부를 판단하려면 `progress >= 0.9f` 조건을 사용해야 합니다.

동기 로딩과 비동기 로딩을 혼용할 때 주의할 점이 있습니다. `SceneManager.LoadScene`은 호출 시점에 진행 중인 모든 `AsyncOperation`을 강제 완료시킵니다. `allowSceneActivation`을 `false`로 설정하여 활성화를 보류한 비동기 로딩이 있더라도 즉시 완료 처리되므로, 의도하지 않은 씬 활성화가 발생할 수 있습니다.

<br>

비동기 로딩이 프레임 드롭을 완전히 제거하지는 않습니다. Unity는 매 프레임 메인 스레드에서 오브젝트 통합에 쓸 수 있는 시간을 제한하지만, 단일 에셋의 통합 작업이 이 시간 예산을 초과하면 해당 프레임에서 스파이크가 발생합니다. 씬 활성화 시점에 호출되는 Awake/Start 콜백에서 무거운 초기화(대량의 오브젝트 생성, 복잡한 데이터 구조 구축 등)를 수행하는 경우에도 스파이크의 원인이 됩니다.

`Application.backgroundLoadingPriority`는 매 프레임 오브젝트 통합에 허용되는 메인 스레드 시간의 상한을 결정합니다. 기본값(`ThreadPriority.Normal`)은 프레임당 최대 10ms입니다. 60 FPS 기준으로 한 프레임의 전체 시간은 약 16.7ms이므로, 통합에 10ms를 쓰면 게임 로직과 렌더링에 남는 시간은 약 6.7ms뿐입니다. `ThreadPriority.Low`로 낮추면 프레임당 통합 시간이 2ms로 줄어들어 프레임 드롭이 완화되지만, 프레임당 처리량이 줄어든 만큼 총 로딩 시간은 길어집니다.

---

## Additive 씬 로딩

지금까지 다룬 씬 로딩은 모두 기존 씬을 파괴하고 새 씬으로 교체하는 LoadSceneMode.Single 방식이었습니다. 이와 달리, **Additive** 모드는 기존 씬을 유지한 채 추가 씬을 함께 로드합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <!-- Title -->
  <text x="350" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Single 모드 vs Additive 모드</text>

  <!-- === Left column: Single === -->
  <rect x="10" y="38" width="330" height="290" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="175" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">LoadSceneMode.Single</text>

  <!-- State 1 -->
  <text x="30" y="92" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 1</text>
  <rect x="85" y="78" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="97" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>

  <!-- Arrow + label -->
  <line x1="130" y1="106" x2="130" y2="148" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="126,145 134,145 130,153" fill="currentColor"/>
  <text x="210" y="132" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">LoadScene("B", Single)</text>

  <!-- State 2 -->
  <text x="30" y="178" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 2</text>
  <rect x="85" y="164" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 B</text>

  <!-- Destroyed Scene A -->
  <rect x="200" y="164" width="90" height="28" rx="5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>
  <text x="245" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.3">씬 A</text>
  <line x1="208" y1="168" x2="282" y2="188" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <line x1="282" y1="168" x2="208" y2="188" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <text x="245" y="210" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">파괴됨</text>

  <!-- === Right column: Additive === -->
  <rect x="360" y="38" width="330" height="290" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">LoadSceneMode.Additive</text>

  <!-- State 1 -->
  <text x="380" y="92" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 1</text>
  <rect x="435" y="78" width="80" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="475" y="97" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>

  <!-- Arrow + label -->
  <line x1="475" y1="106" x2="505" y2="148" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="501,145 509,145 505,153" fill="currentColor"/>
  <text x="555" y="128" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Additive</text>

  <!-- State 2 -->
  <text x="380" y="178" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 2</text>
  <rect x="435" y="164" width="80" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="475" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>
  <text x="523" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">+</text>
  <rect x="535" y="164" width="80" height="28" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="575" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 B</text>

  <!-- Arrow + label -->
  <line x1="525" y1="192" x2="545" y2="234" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="541,231 549,231 545,239" fill="currentColor"/>
  <text x="585" y="218" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Additive</text>

  <!-- State 3 -->
  <text x="380" y="264" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 3</text>
  <rect x="435" y="250" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="469" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>
  <text x="510" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">+</text>
  <rect x="520" y="250" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="554" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 B</text>
  <text x="595" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">+</text>
  <rect x="605" y="250" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="639" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 C</text>

  <text x="525" y="300" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">세 씬 동시 활성화</text>
</svg>
</div>

### Additive 씬의 활용

Additive 씬 로딩을 활용하면 UI, 게임 플레이, 환경을 각각 별도 씬으로 분리하고, 필요한 부분만 독립적으로 로드하거나 교체할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <!-- Title -->
  <text x="350" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Additive 씬 활용 예시</text>

  <!-- === Example 1: UI와 게임 분리 === -->
  <rect x="10" y="38" width="330" height="350" rx="5" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5"/>
  <text x="175" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예시 1: UI와 게임 분리</text>

  <!-- Base Scene -->
  <rect x="25" y="70" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="90" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Base Scene (항상 로드)</text>
  <text x="40" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">게임 매니저</text>
  <text x="155" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이벤트 시스템</text>
  <text x="305" y="90" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">고정</text>

  <!-- UI Scene -->
  <rect x="25" y="150" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="170" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">UI Scene (Additive)</text>
  <text x="40" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Canvas</text>
  <text x="110" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">HUD, 메뉴, 인벤토리</text>
  <text x="305" y="170" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">Additive</text>

  <!-- GamePlay Scene -->
  <rect x="25" y="230" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="250" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GamePlay Scene (Additive)</text>
  <text x="40" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">카메라</text>
  <text x="95" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">조명</text>
  <text x="135" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">플레이어, 적, 환경</text>
  <text x="305" y="250" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">Additive</text>

  <!-- Bracket showing all loaded -->
  <text x="175" y="325" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">세 씬이 동시에 활성화</text>

  <!-- === Example 2: 던전/스테이지 분리 === -->
  <rect x="360" y="38" width="330" height="350" rx="5" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예시 2: 던전/스테이지 분리</text>

  <!-- Persistent Scene -->
  <rect x="375" y="70" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="90" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Persistent Scene</text>
  <text x="390" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">플레이어</text>
  <text x="465" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">UI</text>
  <text x="655" y="90" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">항상 유지</text>

  <!-- Arrow down -->
  <line x1="525" y1="140" x2="525" y2="158" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="521,155 529,155 525,163" fill="currentColor"/>

  <!-- Dungeon Floor 1 (active, solid) -->
  <rect x="375" y="165" width="300" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="185" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Dungeon_Floor_1</text>
  <text x="655" y="185" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">현재 로드</text>
  <text x="390" y="203" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">현재 층의 지형, 적, 오브젝트</text>

  <!-- Swap arrows -->
  <line x1="525" y1="227" x2="525" y2="260" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <polygon points="521,255 529,255 525,263" fill="currentColor" opacity="0.6"/>
  <polygon points="521,232 529,232 525,225" fill="currentColor" opacity="0.6"/>
  <text x="548" y="248" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">교체</text>

  <!-- Dungeon Floor 2 (dashed, next) -->
  <rect x="375" y="265" width="300" height="62" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="390" y="285" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.6">Dungeon_Floor_2</text>
  <text x="655" y="285" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">다음 층 진입 시</text>
  <text x="390" y="303" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">다음 층의 지형, 적, 오브젝트</text>

  <text x="525" y="355" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Persistent Scene은 유지, 콘텐츠 씬만 교체</text>
</svg>
</div>

### SetActiveScene

Additive로 여러 씬이 동시에 로드되어 있으면, 런타임에 생성하는 오브젝트(Instantiate, new GameObject 등)의 소속 씬을 결정해야 합니다.

nity는 **Active Scene**으로 지정된 씬에 새 오브젝트를 소속시키며, `SceneManager.SetActiveScene(scene)`으로 Active Scene을 전환할 수 있습니다.

<br>

```csharp
// 로드된 씬: [UI Scene] + [GamePlay Scene (Active)]

Instantiate(bulletPrefab);
// → bulletPrefab의 인스턴스는 GamePlay Scene에 소속

SceneManager.SetActiveScene(uiScene);

Instantiate(tooltipPrefab);
// → tooltipPrefab의 인스턴스는 UI Scene에 소속

// Active Scene 설정은 오브젝트의 소속 씬을 결정
// 씬 언로드 시 해당 씬에 소속된 오브젝트만 파괴됨
```

<br>

Active Scene을 올바르게 설정해야 하는 이유는 두 가지입니다.

첫째, 오브젝트의 소속 씬이 언로딩 동작에 영향을 줍니다. 특정 씬을 언로드하면 그 씬에 소속된 오브젝트만 파괴됩니다. 오브젝트가 잘못된 씬에 소속되어 있으면, 의도하지 않은 시점에 파괴되거나 파괴되지 않는 문제가 발생합니다.

둘째, Active Scene이 전역 라이팅 설정을 결정합니다. 라이트맵은 각 씬에 독립적으로 베이크되어 Additive로 로드된 씬도 자기 자신의 라이트맵을 사용하지만, 환경 조명·스카이박스·포그 같은 전역 설정은 Active Scene의 것이 적용됩니다. 콘텐츠 씬을 교체할 때 SetActiveScene을 올바른 씬으로 전환하지 않으면, 이전 씬의 환경 라이팅이 그대로 남아 시각적 이상이 발생할 수 있습니다.

---

## DontDestroyOnLoad

씬을 전환(LoadSceneMode.Single)하면 현재 씬의 모든 오브젝트가 파괴됩니다. 그런데 게임 매니저, 오디오 매니저, 네트워크 매니저처럼 게임 전체 수명 동안 유지되어야 하는 오브젝트가 있습니다. `DontDestroyOnLoad(gameObject)`를 호출하면, 해당 오브젝트는 씬 전환 시에도 파괴되지 않고 유지됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 530" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">DontDestroyOnLoad의 동작</text>

  <!-- === 씬 전환 전 === -->
  <text x="20" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 전환 전</text>
  <rect x="10" y="56" width="580" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="76" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Main Menu Scene</text>

  <!-- MenuUI -->
  <rect x="80" y="90" width="170" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="165" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">MenuUI</text>
  <text x="165" y="132" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">일반 오브젝트</text>

  <!-- GameManager (highlighted) -->
  <rect x="330" y="90" width="200" height="56" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="430" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GameManager</text>
  <text x="430" y="132" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">DDOL* 적용</text>

  <!-- Transition arrow -->
  <line x1="300" y1="166" x2="300" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="296,207 304,207 300,215" fill="currentColor"/>
  <text x="320" y="192" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">씬 전환 (LoadScene Single)</text>

  <!-- === 씬 전환 후 === -->
  <text x="20" y="234" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 전환 후</text>

  <!-- Destroyed MenuUI (독립 요소) -->
  <rect x="30" y="248" width="140" height="28" rx="5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.25"/>
  <text x="100" y="266" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.25">MenuUI</text>
  <line x1="38" y1="252" x2="162" y2="272" stroke="currentColor" stroke-width="1.2" opacity="0.3"/>
  <line x1="162" y1="252" x2="38" y2="272" stroke="currentColor" stroke-width="1.2" opacity="0.3"/>
  <text x="185" y="266" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">파괴됨</text>

  <!-- DDOL Scene -->
  <rect x="10" y="290" width="580" height="68" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="24" y="310" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DontDestroyOnLoad (별도 씬)</text>

  <rect x="30" y="318" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="338" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GameManager</text>

  <text x="255" y="338" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">파괴되지 않고 유지</text>

  <!-- Arrow from old GameManager to DDOL -->
  <line x1="430" y1="146" x2="430" y2="200" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <line x1="430" y1="200" x2="130" y2="318" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <polygon points="126,316 134,316 130,323" fill="currentColor" opacity="0.5"/>

  <!-- GamePlay Scene -->
  <rect x="10" y="372" width="580" height="86" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="392" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GamePlay Scene</text>

  <rect x="80" y="402" width="170" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="165" y="427" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Player</text>

  <rect x="330" y="402" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="427" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Environment</text>

  <!-- Summary notes -->
  <text x="300" y="482" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">MenuUI는 씬 전환 시 파괴됨</text>
  <text x="300" y="498" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">GameManager는 DontDestroyOnLoad 씬으로 이동하여 유지</text>
  <text x="300" y="516" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">* DDOL = DontDestroyOnLoad</text>
</svg>
</div>

DontDestroyOnLoad를 호출하면 해당 오브젝트는 기존 씬에서 분리되어, Unity가 내부적으로 관리하는 별도의 **DontDestroyOnLoad 씬**으로 이동합니다. 이 씬은 Hierarchy 창에서 별도로 표시되며, 런타임에서 `gameObject.scene.name`을 확인하면 `"DontDestroyOnLoad"`라는 이름이 반환됩니다.

DontDestroyOnLoad는 **루트 GameObject에만 동작**합니다.
자식 오브젝트에 `DontDestroyOnLoad(childObject)`를 호출하면 Unity는 "DontDestroyOnLoad only works for root GameObjects or components on root GameObjects"라는 경고를 출력하며, 해당 호출은 무시됩니다. 루트 GameObject에 DontDestroyOnLoad를 적용하면, 그 오브젝트의 모든 자식도 함께 보존됩니다.

반대로, DontDestroyOnLoad 씬에 있는 오브젝트를 다시 특정 씬으로 되돌리고 싶다면 `SceneManager.MoveGameObjectToScene(gameObject, targetScene)`을 사용합니다.

이 메서드 역시 루트 GameObject에만 동작하며, 자식 오브젝트에 호출하면 `InvalidOperationException`이 발생합니다. 더 이상 영구 보존할 필요가 없는 오브젝트를 일반 씬으로 옮겨, 해당 씬이 언로드될 때 함께 파괴되도록 할 때 활용합니다.

### 일반적인 사용 대상

DontDestroyOnLoad는 게임 전체 수명 동안 유지되어야 하는 시스템 오브젝트에 사용합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">DontDestroyOnLoad 대표 사용처</text>

  <!-- === 적합한 사용처 (upper, green-ish via low opacity) === -->
  <rect x="10" y="38" width="540" height="206" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">적합한 사용처</text>

  <!-- Item 1 -->
  <rect x="25" y="74" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="94" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GameManager</text>
  <text x="200" y="94" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">게임 상태 관리 (점수, 진행도)</text>

  <!-- Item 2 -->
  <rect x="25" y="110" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="130" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">AudioManager</text>
  <text x="200" y="130" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">BGM 끊김 없이 재생</text>

  <!-- Item 3 -->
  <rect x="25" y="146" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="166" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">NetworkManager</text>
  <text x="200" y="166" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">서버 연결 유지</text>

  <!-- Item 4 -->
  <rect x="25" y="182" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="202" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">InputManager</text>
  <text x="200" y="202" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">입력 설정 유지</text>

  <!-- Item 5 -->
  <rect x="25" y="218" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="238" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">EventSystem</text>
  <text x="200" y="238" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">UI 이벤트 처리 (주의: 중복 방지 필요)</text>

  <!-- === 부적합한 사용처 (lower, red-ish via higher opacity) === -->
  <rect x="10" y="258" width="540" height="120" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="282" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">부적합한 사용처</text>

  <!-- Item 1 -->
  <rect x="25" y="292" width="510" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="310" font-family="sans-serif" font-size="11" fill="currentColor">특정 씬에서만 필요한 오브젝트</text>

  <!-- Item 2 -->
  <rect x="25" y="322" width="510" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="340" font-family="sans-serif" font-size="11" fill="currentColor">임시 데이터를 가진 오브젝트</text>

  <!-- Item 3 -->
  <rect x="25" y="352" width="510" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="370" font-family="sans-serif" font-size="11" fill="currentColor">UI 요소 (특정 화면의 UI)</text>
</svg>
</div>

EventSystem을 DontDestroyOnLoad로 설정하는 경우, 새 씬에도 EventSystem이 있으면 두 개가 동시에 존재하게 됩니다.
Unity는 하나의 활성 EventSystem만 허용하므로, 중복을 감지하여 자기 자신을 파괴하는 로직을 추가해야 합니다.

반대로, 특정 화면에서만 쓰이는 UI 패널이나 임시 이펙트처럼 수명이 한정된 오브젝트에 DontDestroyOnLoad를 적용하면, 씬이 바뀐 뒤에도 메모리에 남아 낭비로 이어집니다.

### 싱글턴 중복 인스턴스 문제

DontDestroyOnLoad 오브젝트는 대부분 싱글턴 패턴으로 구현됩니다. 그런데 씬 A에서 GameManager를 DontDestroyOnLoad로 등록한 뒤, 게임 도중 씬 A로 다시 돌아오면 씬 A가 새로 로드되면서 GameManager가 한 번 더 생성됩니다. 기존 인스턴스는 DontDestroyOnLoad 씬에 이미 존재하므로, 두 개의 GameManager가 동시에 존재하게 됩니다. 이 중복을 방지하려면 Awake에서 기존 인스턴스 여부를 확인하고, 이미 존재하면 새로 생성된 자신을 즉시 파괴하는 로직이 필요합니다.

<br>

### 남용 시 메모리 누수 위험

DontDestroyOnLoad 오브젝트에서 대량의 텍스처나 오디오 클립을 직접 참조하고 있으면, 그 에셋들은 씬 전환과 무관하게 게임 전체 수명 동안 메모리에 상주합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- AudioManager 루트 박스 -->
  <rect x="145" y="10" width="230" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="30" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">AudioManager</text>
  <text x="260" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(DontDestroyOnLoad)</text>

  <!-- 중앙 수직선 -->
  <line x1="260" y1="54" x2="260" y2="78" stroke="currentColor" stroke-width="1.5"/>
  <!-- 수평 분기선 -->
  <line x1="70" y1="78" x2="450" y2="78" stroke="currentColor" stroke-width="1.5"/>
  <!-- 각 노드로 수직선 + 화살표 -->
  <line x1="70" y1="78" x2="70" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="67,96 70,102 73,96" fill="currentColor"/>
  <line x1="197" y1="78" x2="197" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="194,96 197,102 200,96" fill="currentColor"/>
  <line x1="323" y1="78" x2="323" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="320,96 323,102 326,96" fill="currentColor"/>
  <line x1="450" y1="78" x2="450" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="447,96 450,102 453,96" fill="currentColor"/>

  <!-- BGM 1: MainMenu -->
  <rect x="10" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_MainMenu</text>
  <text x="70" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (3MB)</text>
  <text x="70" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">메인 메뉴에서만 필요</text>

  <!-- BGM 2: GamePlay -->
  <rect x="137" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="197" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_GamePlay</text>
  <text x="197" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (5MB)</text>
  <text x="197" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">게임 중에만 필요</text>

  <!-- BGM 3: Boss -->
  <rect x="263" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="323" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_Boss</text>
  <text x="323" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (4MB)</text>
  <text x="323" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">보스전에서만 필요</text>

  <!-- BGM 4: Ending -->
  <rect x="390" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_Ending</text>
  <text x="450" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (3MB)</text>
  <text x="450" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">엔딩에서만 필요</text>

  <!-- 구분선 -->
  <line x1="30" y1="190" x2="490" y2="190" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- 합계 강조 박스 -->
  <rect x="130" y="204" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="220" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">3 + 5 + 4 + 3 = 15MB</text>
  <text x="260" y="234" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">항상 메모리에 상주</text>

  <!-- 화살표: 합계 → 해결 -->
  <line x1="260" y1="240" x2="260" y2="260" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="257,260 260,266 263,260" fill="currentColor"/>

  <!-- 해결 방안 박스 (점선) -->
  <rect x="80" y="268" width="360" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="260" y="288" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">해결: BGM을 직접 참조하지 않고</text>
  <text x="260" y="306" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">필요 시 Addressables로 동적 로드/해제</text>

  <!-- 보조 텍스트 -->
  <text x="260" y="350" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">DDOL 오브젝트가 에셋을 직접 참조하면 씬 전환과 무관하게 메모리 점유</text>
</svg>
</div>

DontDestroyOnLoad 오브젝트는 가능한 한 가볍게 유지해야 합니다. 에셋 데이터를 직접 참조하지 않고 Addressables 등으로 동적 로드/해제하며, 씬별로 필요한 리소스는 해당 씬에서만 로드하는 것이 원칙입니다. 적용 대상의 수 자체도 최소한으로 제한해야 합니다.

---

## 씬 언로딩과 메모리 해제

씬을 전환하거나 Additive 씬을 제거할 때, 메모리가 즉시 해제되지는 않습니다. 오브젝트 파괴와 에셋 메모리 해제는 별도의 과정이기 때문입니다.

### 오브젝트 파괴 vs 에셋 해제

씬을 언로드하면 그 씬에 소속된 GameObject와 컴포넌트가 파괴됩니다. 파괴되는 오브젝트에서 실행 중이던 **코루틴(Coroutine)**은 자동으로 중단됩니다. 코루틴은 MonoBehaviour가 소유하고 실행하는 함수이므로, 해당 오브젝트와 생명주기를 공유하기 때문입니다.

반면, 해당 오브젝트가 다른 시스템에 등록한 이벤트 핸들러(예: 버튼의 onClick, C# 이벤트 구독 등)는 자동으로 해제되지 않습니다. 이벤트 시스템은 구독자의 생존 여부를 추적하지 않기 때문입니다. 파괴된 오브젝트의 메서드를 콜백으로 여전히 참조하게 되면 MissingReferenceException이 발생하므로, OnDestroy에서 이벤트 구독을 해제하는 것이 안전합니다.

오브젝트가 파괴되어도, 그 오브젝트가 참조하던 에셋(텍스처, 메쉬, 오디오 클립 등)의 메모리는 **즉시 해제되지 않습니다.**

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 타이틀 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 A 언로드 시</text>

  <!-- ===== 단계 1: 오브젝트 파괴 ===== -->
  <rect x="10" y="34" width="540" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="56" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">단계 1 — 오브젝트 파괴</text>

  <!-- GO 박스들 (파괴됨) -->
  <rect x="30" y="68" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="90" y="89" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Player (파괴)</text>

  <rect x="30" y="108" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="90" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Enemy (파괴)</text>

  <rect x="30" y="148" width="140" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="100" y="169" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Environment (파괴)</text>

  <!-- 괄호 + 콜백 텍스트 -->
  <line x1="180" y1="78" x2="195" y2="78" stroke="currentColor" stroke-width="1"/>
  <line x1="180" y1="124" x2="195" y2="124" stroke="currentColor" stroke-width="1"/>
  <line x1="180" y1="164" x2="195" y2="164" stroke="currentColor" stroke-width="1"/>
  <line x1="195" y1="78" x2="195" y2="164" stroke="currentColor" stroke-width="1"/>
  <line x1="195" y1="124" x2="210" y2="124" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,121 216,124 210,127" fill="currentColor"/>
  <text x="222" y="128" font-family="sans-serif" font-size="10" fill="currentColor">OnDisable, OnDestroy 호출</text>

  <!-- 에셋 잔류 표시 -->
  <rect x="370" y="68" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="89" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Texture_A</text>

  <rect x="370" y="108" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Mesh_B</text>

  <rect x="370" y="148" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="169" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Audio_C</text>

  <text x="450" y="198" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">메모리에 잔류</text>

  <!-- 단계 1→2 화살표 -->
  <line x1="280" y1="214" x2="280" y2="244" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="277,244 280,250 283,244" fill="currentColor"/>

  <!-- ===== 단계 2: 에셋 해제 ===== -->
  <rect x="10" y="254" width="540" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="276" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">단계 2 — 에셋 해제 (별도 호출 필요)</text>

  <!-- UnloadUnusedAssets 호출 박스 -->
  <rect x="30" y="290" width="310" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="185" y="310" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Resources.UnloadUnusedAssets()</text>

  <!-- 화살표 → 해제 결과 -->
  <line x1="345" y1="305" x2="370" y2="305" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="370,302 376,305 370,308" fill="currentColor"/>

  <!-- 해제 결과 텍스트 -->
  <text x="382" y="298" font-family="sans-serif" font-size="10" fill="currentColor">참조 없는 에셋 해제:</text>
  <text x="382" y="314" font-family="sans-serif" font-size="10" fill="currentColor">Texture_A, Mesh_B, Audio_C</text>

  <!-- 해제 완료 아이콘 표시 (점선 박스) -->
  <rect x="370" y="330" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="450" y="344" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Texture_A — 해제됨</text>
  <text x="450" y="356" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Mesh_B, Audio_C — 해제됨</text>

  <!-- 주의 텍스트 -->
  <rect x="30" y="334" width="320" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="40" y="352" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">※ 다른 씬이나 DDOL 오브젝트가 참조 중이면 해제되지 않음</text>

  <!-- 하단 보조 텍스트 -->
  <text x="280" y="440" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">오브젝트 파괴와 에셋 메모리 해제는 별도 과정</text>
</svg>
</div>

오브젝트가 파괴되면 그 오브젝트의 에셋 참조는 사라지지만, 다른 오브젝트나 DDOL 씬에서 같은 에셋을 여전히 참조하고 있을 수 있습니다. Unity는 `Resources.UnloadUnusedAssets()`를 통해 모든 참조를 확인한 뒤에야 에셋 메모리를 해제합니다.

### Resources.UnloadUnusedAssets()

이 함수는 현재 메모리에 로드된 에셋들의 **참조 상태를 추적**하여, 어디에서도 참조되지 않는 에셋을 메모리에서 해제합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">UnloadUnusedAssets() 동작</text>

  <!-- Outer border -->
  <rect x="10" y="38" width="540" height="156" rx="5" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5"/>

  <!-- Header background -->
  <rect x="11" y="39" width="538" height="26" fill="currentColor" fill-opacity="0.08"/>

  <!-- Header texts -->
  <text x="85" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">에셋</text>
  <text x="290" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">참조 상태</text>
  <text x="490" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">결과</text>

  <!-- Header bottom line -->
  <line x1="10" y1="65" x2="550" y2="65" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- Column separators -->
  <line x1="165" y1="39" x2="165" y2="193" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <line x1="430" y1="39" x2="430" y2="193" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>

  <!-- Row 1: Texture_A — 해제 -->
  <text x="85" y="86" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor" opacity="0.4">Texture_A</text>
  <text x="290" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">참조 없음</text>
  <text x="490" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">해제</text>

  <line x1="10" y1="97" x2="550" y2="97" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>

  <!-- Row 2: Texture_B — 유지 -->
  <rect x="11" y="98" width="538" height="31" fill="currentColor" fill-opacity="0.04"/>
  <text x="85" y="118" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">Texture_B</text>
  <text x="290" y="118" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Player가 참조</text>
  <text x="490" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">유지</text>

  <line x1="10" y1="129" x2="550" y2="129" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>

  <!-- Row 3: Mesh_C — 해제 -->
  <text x="85" y="150" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor" opacity="0.4">Mesh_C</text>
  <text x="290" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">참조 없음</text>
  <text x="490" y="150" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">해제</text>

  <line x1="10" y1="161" x2="550" y2="161" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>

  <!-- Row 4: Audio_D — 유지 -->
  <rect x="11" y="162" width="538" height="31" fill="currentColor" fill-opacity="0.04"/>
  <text x="85" y="182" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">Audio_D</text>
  <text x="290" y="182" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">AudioManager가 참조 (DDOL)</text>
  <text x="490" y="182" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">유지</text>

  <!-- Footer -->
  <text x="280" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">비동기 실행 (AsyncOperation 반환) · 참조 추적에 수백 ms 소요 가능</text>
  <text x="280" y="238" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">프레임 스파이크 유발 가능 → 로딩 화면 중 호출 권장</text>
</svg>
</div>

UnloadUnusedAssets는 비용이 높은 연산입니다. 프로젝트에 에셋이 많을수록 추적 시간이 길어지며, 매 프레임 호출하면 성능 저하를 유발합니다.

### GC.Collect와의 관계

**가비지 컬렉션(Garbage Collection)**은 C#의 **관리 힙(Managed Heap)**에서 더 이상 도달할 수 없는(unreachable) 객체를 수거하는 과정이며, `GC.Collect()`는 이를 즉시 실행하는 함수입니다.

UnloadUnusedAssets의 참조 추적이 정확하려면 관리 힙의 도달 불가능한 객체가 먼저 수거되어야 하므로, UnloadUnusedAssets는 내부적으로 `GC.Collect()`를 호출합니다. 개발자가 별도로 `GC.Collect()`를 호출할 필요는 없습니다.

Unity에서 텍스처나 메쉬 같은 에셋의 실제 데이터는 네이티브(C++) 메모리에 저장되고, C# 코드에서는 Texture2D, Mesh 같은 래퍼 객체를 통해 이를 참조합니다.

씬이 언로드되면 GameObject와 컴포넌트는 파괴되어 `== null`이 `true`를 반환하지만, 가비지 컬렉터가 수거하기 전까지 관리 힙에는 남아 있습니다.

이 객체가 참조하던 Texture2D 래퍼도 도달 가능한 상태로 유지되어, Unity는 해당 네이티브 에셋을 아직 사용 중으로 판단합니다.

`GC.Collect()`를 실행해야 이런 객체들이 수거되고, 네이티브 에셋에 대한 참조가 완전히 제거되어 비로소 해제 대상이 됩니다.

### 씬 전환 시 전체 흐름

씬 전환의 최적 패턴은 로딩 화면을 경유하는 것입니다.
[메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 다룬 메모리 피크 관리와 직접 연결됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 540" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- ===== 상단: 5단계 순서도 ===== -->
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 전환 시 권장 흐름</text>

  <!-- 단계 1 -->
  <rect x="10" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="64" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. 로딩 씬</text>
  <text x="64" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Additive 로드</text>
  <text x="64" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">로딩 화면 표시</text>

  <!-- 화살표 1→2 -->
  <line x1="118" y1="64" x2="138" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="138,61 144,64 138,67" fill="currentColor"/>

  <!-- 단계 2 -->
  <rect x="146" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. 이전 씬</text>
  <text x="200" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">언로드</text>
  <text x="200" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">오브젝트 파괴</text>

  <!-- 화살표 2→3 -->
  <line x1="254" y1="64" x2="274" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="274,61 280,64 274,67" fill="currentColor"/>

  <!-- 단계 3 -->
  <rect x="282" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="336" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. 미사용</text>
  <text x="336" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">에셋 해제</text>
  <text x="336" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">UnloadUnusedAssets</text>

  <!-- 화살표 3→4 -->
  <line x1="390" y1="64" x2="410" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="410,61 416,64 410,67" fill="currentColor"/>

  <!-- 단계 4 -->
  <rect x="418" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="472" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4. 새 씬</text>
  <text x="472" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">비동기 로드</text>
  <text x="472" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">progress 로딩 바</text>

  <!-- 화살표 4→5 -->
  <line x1="526" y1="64" x2="546" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="546,61 552,64 546,67" fill="currentColor"/>

  <!-- 단계 5 -->
  <rect x="554" y="30" width="56" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="582" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">5.</text>
  <text x="582" y="66" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">로딩 씬</text>
  <text x="582" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">언로드</text>

  <!-- yield return 보조 텍스트 -->
  <text x="310" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">각 단계에서 yield return으로 완료를 대기 → 다음 단계가 올바른 상태에서 시작</text>

  <!-- ===== 구분선 ===== -->
  <line x1="30" y1="132" x2="590" y2="132" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- ===== 하단: 메모리 그래프 ===== -->
  <text x="310" y="154" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">메모리 변화</text>

  <!-- Y축 -->
  <line x1="60" y1="175" x2="60" y2="420" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="300" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" transform="rotate(-90, 30, 300)">메모리</text>

  <!-- X축 -->
  <line x1="60" y1="420" x2="590" y2="420" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="442" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">시간 / 단계</text>

  <!-- 메모리 꺾은선 그래프 -->
  <!-- 기준선 (이전 씬) -->
  <polyline points="60,340 120,340 160,220 200,200 240,220 300,340 340,380 400,380 440,300 500,280 560,280 590,280"
    fill="none" stroke="currentColor" stroke-width="2"/>

  <!-- 피크 영역 음영 -->
  <polygon points="120,340 160,220 200,200 240,220 300,340 120,340"
    fill="currentColor" fill-opacity="0.08"/>

  <!-- 새 씬 로드 영역 음영 -->
  <polygon points="400,380 440,300 500,280 560,280 590,280 590,380 400,380"
    fill="currentColor" fill-opacity="0.06"/>

  <!-- 피크 레이블 -->
  <line x1="200" y1="200" x2="200" y2="178" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="200" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">피크</text>

  <!-- 단계 1 레이블: 로딩 씬 추가 -->
  <text x="140" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">① 로딩 씬</text>
  <text x="140" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">추가 로드</text>
  <line x1="140" y1="420" x2="140" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 2 레이블: 이전 씬 언로드 -->
  <text x="230" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">② 이전 씬</text>
  <text x="230" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">언로드</text>
  <line x1="230" y1="420" x2="230" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 3 레이블: 에셋 해제 -->
  <text x="340" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">③ 이전 에셋 해제</text>
  <text x="340" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">메모리 여유 확보</text>
  <line x1="340" y1="380" x2="340" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 4 레이블: 새 씬 로드 -->
  <text x="470" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">④ 새 에셋 로드</text>
  <line x1="470" y1="420" x2="470" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 5 레이블: 로딩 씬 제거 -->
  <text x="565" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">⑤ 로딩 씬</text>
  <text x="565" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">언로드</text>
  <line x1="565" y1="420" x2="565" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 핵심 강조 텍스트 -->
  <text x="310" y="510" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">핵심: 이전 에셋 해제 후 새 에셋 로드 → 두 씬 에셋 동시 상주 구간(피크) 최소화</text>
  <text x="310" y="526" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Additive 씬 언로드 시 UnloadUnusedAssets 자동 호출 없음 → 명시 호출 필수</text>
</svg>
</div>

3단계의 `Resources.UnloadUnusedAssets()` 명시 호출은 필수입니다. `LoadScene(Single)` 방식에서는 Unity가 새 씬 로드 후 `UnloadUnusedAssets`를 자동으로 호출하지만, `UnloadSceneAsync`(Additive 씬 언로드)에서는 자동 호출이 없습니다.
따라서 Additive 기반 씬 전환에서는 개발자가 직접 호출해야 이전 씬의 에셋이 해제됩니다.

각 단계 사이에 `yield return`(코루틴) 또는 `await`(async/await)로 완료를 대기하는 것도 필수입니다.
`UnloadSceneAsync`와 `UnloadUnusedAssets`는 모두 비동기로 실행되므로, 완료를 기다리지 않고 다음 단계를 시작하면 이전 에셋이 해제되기 전에 새 에셋이 로드되어 메모리 피크가 줄어들지 않습니다.

메모리 피크가 높아지면 모바일에서 **OOM(Out Of Memory)**이 발생할 수 있습니다. OOM은 앱의 메모리 사용량이 OS 허용 한도를 초과했을 때 OS가 앱을 강제 종료하는 현상입니다. 모바일 기기의 RAM이 4~8GB이더라도 OS가 앱 하나에 허용하는 메모리는 대체로 1~2GB 수준이므로, 두 씬의 에셋이 겹치는 순간 이 한도를 넘기기 쉽습니다.

---

## 대규모 월드를 위한 씬 분할 전략

지금까지 다룬 씬 전환 패턴은 메뉴 → 게임 → 결과처럼 단계가 명확히 나뉘는 구조에 적합합니다. 오픈 월드나 대규모 맵을 가진 게임에서는 전체 월드를 하나의 씬에 담을 수 없습니다. 에셋 총량이 기기의 메모리 한계를 초과하기 때문입니다.

이 문제를 해결하는 방법이 **씬 분할(Scene Splitting)**입니다.

<br>

### 그리드 기반 월드 분할

월드를 격자(Grid)로 나누어 각 셀을 별도의 씬으로 구성합니다. 플레이어 위치에 따라 현재 셀과 인접 셀만 Additive로 로드하고, 로드 범위를 벗어난 셀은 언로드하면 전체 월드 중 플레이어 주변의 에셋만 메모리에 유지됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <text x="210" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">그리드 기반 씬 분할</text>

  <!-- 로드 범위 점선 -->
  <rect x="30" y="40" width="360" height="240" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="6,3"/>

  <!-- Row 0 -->
  <rect x="40" y="50" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_00</text>
  <text x="95" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="155" y="50" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_01</text>
  <text x="210" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="270" y="50" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_02</text>
  <text x="325" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>

  <!-- Row 1 -->
  <rect x="40" y="125" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="157" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_10</text>
  <text x="95" y="171" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <!-- Cell_11 강조 -->
  <rect x="155" y="125" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="2"/>
  <text x="193" y="155" text-anchor="middle" font-family="sans-serif" font-size="15" fill="currentColor">★</text>
  <text x="230" y="157" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_11</text>
  <text x="210" y="175" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">플레이어 위치</text>
  <rect x="270" y="125" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="157" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_12</text>
  <text x="325" y="171" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>

  <!-- Row 2 -->
  <rect x="40" y="200" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_20</text>
  <text x="95" y="246" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="155" y="200" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_21</text>
  <text x="210" y="246" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="270" y="200" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_22</text>
  <text x="325" y="246" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>

  <!-- 하단 설명 -->
  <text x="210" y="300" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">플레이어가 Cell_11에 위치할 때: 3×3 범위 전체 로드</text>
  <text x="210" y="325" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">로드 : Cell_00 ~ Cell_22 (3×3 = 9개 셀)</text>
  <text x="210" y="342" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">언로드 : 3×3 범위 밖의 셀</text>
  <text x="210" y="362" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">점선 = 로드 범위 경계</text>
</svg>
</div>

### 스트리밍: 미리 로드하기

플레이어가 셀 사이를 이동하면 로드 범위도 함께 이동합니다. **스트리밍(Streaming)**은 플레이어가 셀 경계에 가까워질 때 이동 방향의 인접 셀을 미리 비동기 로드하고, 반대쪽 셀을 언로드하여 끊김 없이 월드를 탐색할 수 있게 하는 방식입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <text x="340" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 스트리밍 동작</text>

  <!-- 타임라인 축 -->
  <line x1="30" y1="52" x2="650" y2="52" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="648,48 656,52 648,56" fill="currentColor"/>
  <text x="665" y="56" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">시간</text>

  <!-- t0 마커 -->
  <line x1="110" y1="45" x2="110" y2="59" stroke="currentColor" stroke-width="2"/>
  <text x="110" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">t0</text>

  <!-- t1 마커 -->
  <line x1="340" y1="45" x2="340" y2="59" stroke="currentColor" stroke-width="2"/>
  <text x="340" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">t1</text>

  <!-- t2 마커 -->
  <line x1="560" y1="45" x2="560" y2="59" stroke="currentColor" stroke-width="2"/>
  <text x="560" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">t2</text>

  <!-- t0: 3x3 그리드 (Cell_00~22 모두 로드) -->
  <!-- Row 0 -->
  <rect x="50" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="69" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">00</text>
  <rect x="91" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">01</text>
  <rect x="132" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="151" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">02</text>
  <!-- Row 1 -->
  <rect x="50" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="69" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">10</text>
  <rect x="91" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="114" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">★11</text>
  <rect x="132" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="151" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">12</text>
  <!-- Row 2 -->
  <rect x="50" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="69" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">20</text>
  <rect x="91" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">21</text>
  <rect x="132" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="151" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">22</text>

  <text x="110" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">3×3 모두 로드</text>
  <text x="110" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">플레이어 Cell_11 중앙</text>

  <!-- 화살표 t0→t1 -->
  <line x1="185" y1="110" x2="255" y2="110" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <polygon points="253,107 260,110 253,113" fill="currentColor"/>

  <!-- t1: 3x3 + 새 열 로딩 시작 -->
  <!-- Row 0 -->
  <rect x="275" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="294" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">00</text>
  <rect x="316" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="335" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">01</text>
  <rect x="357" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="376" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">02</text>
  <!-- 새로 로드 시작: 03 -->
  <rect x="398" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="417" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">03</text>
  <!-- Row 1 -->
  <rect x="275" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="294" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">10</text>
  <rect x="316" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="335" y="114" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">★11</text>
  <rect x="357" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="376" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">12</text>
  <!-- 새로 로드 시작: 13 -->
  <rect x="398" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="417" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">13</text>
  <!-- Row 2 -->
  <rect x="275" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="294" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">20</text>
  <rect x="316" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="335" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">21</text>
  <rect x="357" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="376" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">22</text>
  <!-- 새로 로드 시작: 23 -->
  <rect x="398" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="417" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">23</text>

  <text x="350" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Cell_12 방향 이동 감지</text>
  <text x="350" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">03/13/23 비동기 로드 시작 (점선)</text>

  <!-- 화살표 t1→t2 -->
  <line x1="448" y1="110" x2="485" y2="110" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <polygon points="483,107 490,110 483,113" fill="currentColor"/>

  <!-- t2: 새 3x3 (01~23), 00/10/20 언로드 -->
  <!-- Row 0: 00 언로드 (흐림) -->
  <rect x="495" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="514" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.3">00</text>
  <rect x="536" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="555" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">01</text>
  <rect x="577" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="596" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">02</text>
  <rect x="618" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="637" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">03</text>
  <!-- Row 1: 10 언로드 -->
  <rect x="495" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="514" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.3">10</text>
  <rect x="536" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="555" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">11</text>
  <rect x="577" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="596" y="114" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">★12</text>
  <rect x="618" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="637" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">13</text>
  <!-- Row 2: 20 언로드 -->
  <rect x="495" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="514" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.3">20</text>
  <rect x="536" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="555" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">21</text>
  <rect x="577" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="596" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">22</text>
  <rect x="618" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="637" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">23</text>

  <text x="570" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">플레이어 Cell_12 진입</text>
  <text x="570" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">03/13/23 로드 완료, 00/10/20 언로드</text>

  <!-- 범례 -->
  <rect x="120" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="209" font-family="sans-serif" font-size="9" fill="currentColor">새로 로드</text>
  <rect x="220" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="240" y="209" font-family="sans-serif" font-size="9" fill="currentColor">언로드</text>
  <rect x="310" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="330" y="209" font-family="sans-serif" font-size="9" fill="currentColor">로딩 중</text>
  <rect x="400" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="420" y="209" font-family="sans-serif" font-size="9" fill="currentColor">로드 유지</text>

  <!-- 하단 결론 -->
  <text x="340" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">플레이어 시점에서 끊김 없이 월드가 이어짐</text>
  <text x="340" y="256" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">항상 일정 범위의 셀만 메모리에 유지</text>
</svg>
</div>

플레이어가 현재 셀을 이동하는 동안, 이동 방향의 다음 셀이 백그라운드에서 비동기 로드됩니다.
셀 경계에 도착할 때 로딩이 이미 완료되어 있으면 끊김 없이 새 영역이 나타납니다. 비동기 로딩은 셀의 에셋 양에 따라 수백 ms에서 수 초까지 걸리므로, 플레이어의 이동 속도와 로딩 시간을 고려하여 경계 도달 전에 충분한 여유를 두고 로딩을 시작해야 합니다.
로딩이 완료되기 전에 플레이어가 새 셀에 진입하면, 빈 공간이 보이거나 오브젝트가 갑자기 나타나는 팝인(pop-in)이 발생합니다.

메모리 측면에서는 로드된 셀의 총 수가 항상 일정하게 유지됩니다. 위 예시에서 로드 범위가 3×3이면 항상 9개 셀의 에셋만 메모리에 올라가므로, 월드 전체 크기와 무관하게 메모리 사용량의 상한을 예측할 수 있습니다.

### 씬 간 공유 에셋 관리

인접한 셀들은 같은 나무 프리팹이나 지형 텍스처를 공유하는 경우가 많습니다. 각 셀을 AssetBundle로 패키징할 때, 공유 에셋을 별도 번들로 분리하지 않으면 동일한 에셋이 셀마다 복사되어 메모리에 중복으로 올라갑니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">공유 에셋 문제와 해결</text>

  <!-- 문제 섹션 -->
  <rect x="20" y="38" width="480" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="58" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">문제: 공유 에셋을 별도 번들로 분리하지 않은 경우</text>

  <!-- Cell_11 번들 -->
  <rect x="35" y="70" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="105" y="87" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Cell_11 번들</text>
  <text x="105" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Tree_A (4MB)</text>

  <!-- Cell_12 번들 -->
  <rect x="190" y="70" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="87" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Cell_12 번들</text>
  <text x="260" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Tree_A (4MB)</text>

  <!-- Cell_21 번들 -->
  <rect x="345" y="70" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="415" y="87" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Cell_21 번들</text>
  <text x="415" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Tree_A (4MB)</text>

  <!-- 중복 표시 -->
  <text x="213" y="133" font-family="sans-serif" font-size="11" fill="currentColor">같은 에셋 3벌 복사</text>
  <text x="400" y="133" font-family="sans-serif" font-size="11" fill="currentColor">= 12MB</text>
  <text x="470" y="155" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">✕</text>

  <!-- 해결 섹션 -->
  <text x="260" y="195" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">해결 방안</text>

  <!-- 해결 1 -->
  <rect x="20" y="208" width="155" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="97" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">해결 1</text>
  <text x="97" y="244" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">씬 직접 참조</text>
  <text x="97" y="258" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">(번들 미사용)</text>
  <text x="97" y="278" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">같은 GUID → 1회 로드</text>

  <!-- 해결 2 -->
  <rect x="183" y="208" width="155" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">해결 2</text>
  <text x="260" y="244" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">AssetBundle</text>
  <text x="260" y="258" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">공유 번들 분리</text>
  <text x="260" y="278" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">의존성 기록만, 복사 없음</text>

  <!-- 해결 3 -->
  <rect x="345" y="208" width="155" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="422" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">해결 3</text>
  <text x="422" y="244" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Addressables</text>
  <text x="422" y="258" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">별도 그룹 분리</text>
  <text x="422" y="278" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">참조 카운팅 → 1회 로드</text>

  <!-- 공통 결과 -->
  <!-- 화살표: 해결1 → 결과 -->
  <line x1="97" y1="288" x2="97" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="260" y1="288" x2="260" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="422" y1="288" x2="422" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="97" y1="300" x2="422" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="260" y1="300" x2="260" y2="312" stroke="currentColor" stroke-width="1"/>
  <polygon points="256,310 260,318 264,310" fill="currentColor"/>

  <rect x="155" y="320" width="210" height="32" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="341" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">메모리 사용: 4MB (1회 로드)</text>
</svg>
</div>

Unity는 같은 에셋 파일(같은 GUID)을 참조하면 메모리에 한 번만 로드합니다.

AssetBundle은 번들 단위로 독립된 파일을 생성합니다. 위 예시에서 Tree_A가 Cell_11 번들에도 Cell_12 번들에도 필요한데 어떤 번들에도 배정되어 있지 않으면, Unity는 런타임에 Tree_A를 찾을 곳이 없으므로 각 번들 안에 데이터를 복사합니다.
복사된 데이터는 번들마다 별개이므로, 두 번들을 동시에 로드하면 같은 에셋이 메모리에 두 벌 존재합니다.

Tree_A를 별도의 공유 번들에 배정하면, 각 셀 번들에는 "공유 번들에서 로드"라는 의존성 기록만 남아 에셋이 한 번만 
로드됩니다.
Addressables의 그룹 구성과 의존성 분석 기능을 활용하면 이 문제를 체계적으로 관리할 수 있습니다. 구체적인 방법은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 다룹니다.

### 공통 씬과 콘텐츠 씬 분리

대규모 프로젝트에서는 씬을 **공통 씬(Persistent Scene)**과 **콘텐츠 씬(Content Scene)**으로 분리하는 구조가 일반적입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">공통 씬 + 콘텐츠 씬 구조</text>
  <rect x="40" y="40" width="400" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Persistent Scene (항상 로드)</text>
  <text x="70" y="84" font-family="sans-serif" font-size="11" fill="currentColor">플레이어 캐릭터</text>
  <text x="70" y="100" font-family="sans-serif" font-size="11" fill="currentColor">카메라 시스템</text>
  <text x="70" y="116" font-family="sans-serif" font-size="11" fill="currentColor">게임 매니저</text>
  <text x="250" y="84" font-family="sans-serif" font-size="11" fill="currentColor">UI</text>
  <text x="250" y="100" font-family="sans-serif" font-size="11" fill="currentColor">조명 (글로벌)</text>
  <line x1="240" y1="160" x2="240" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="236,196 240,204 244,196" fill="currentColor"/>
  <polygon points="236,164 240,156 244,164" fill="currentColor"/>
  <text x="340" y="183" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Additive 로드 / 언로드</text>
  <rect x="40" y="210" width="400" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="240" y="232" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Content Scene (교체)</text>
  <text x="70" y="254" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 지형</text>
  <text x="70" y="270" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 적 배치</text>
  <text x="270" y="254" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 오브젝트</text>
  <text x="270" y="270" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 조명 (로컬)</text>
  <text x="240" y="305" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">점선 = 교체 가능한 씬</text>
  <rect x="40" y="335" width="400" height="78" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="240" y="355" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스테이지 전환 흐름</text>
  <text x="60" y="375" font-family="sans-serif" font-size="10" fill="currentColor">1. Content Scene (Stage 1) 언로드</text>
  <text x="60" y="391" font-family="sans-serif" font-size="10" fill="currentColor">2. UnloadUnusedAssets()</text>
  <text x="60" y="407" font-family="sans-serif" font-size="10" fill="currentColor">3. Content Scene (Stage 2) 비동기 로드</text>
  <text x="310" y="407" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 플레이어, UI는 유지됨</text>
</svg>
</div>

공통 씬에는 씬 전환과 무관하게 유지되어야 하는 오브젝트를, 콘텐츠 씬에는 스테이지별로 달라지는 요소만 배치합니다. 스테이지 전환 시 콘텐츠 씬만 교체하므로 공통 요소의 재로딩이 발생하지 않습니다.

DontDestroyOnLoad 씬은 Unity가 내부적으로 관리하므로 개발자가 씬 자체를 언로드할 수 없고, 오브젝트를 해제하려면 하나씩 `Destroy()`를 호출해야 합니다. 공통 씬 방식에서는 씬의 로드/언로드 시점을 개발자가 직접 제어하므로, 공통 씬을 언로드하면 그 안의 모든 오브젝트가 함께 파괴됩니다.

---

## 마무리

- 동기 로딩은 메인 스레드를 블로킹하여 프레임 정지를 유발하며, 비동기 로딩은 여러 프레임에 걸쳐 작업을 분산합니다. allowSceneActivation으로 활성화 시점을 제어할 수 있습니다.
- Additive 씬 로딩으로 UI, 게임플레이, 환경을 독립된 씬으로 분리하여 개별적으로 로드/언로드할 수 있습니다.
- DontDestroyOnLoad는 씬 전환 시 오브젝트를 유지하지만, 참조 에셋이 해제되지 않으므로 최소한으로 사용해야 합니다.
- 오브젝트 파괴 후에도 에셋 메모리는 즉시 해제되지 않으며, Resources.UnloadUnusedAssets()로 명시적 해제가 필요합니다.
- 대규모 월드에서는 그리드 씬 분할과 공통 씬/콘텐츠 씬 분리로 메모리 사용량의 상한을 예측 가능하게 유지합니다.

씬 관리의 본질은 메모리의 할당과 해제 시점을 제어하는 것입니다. 어떤 에셋을 언제 로드하고 언제 해제할지, 씬 전환 시 메모리 피크를 어떻게 최소화할지가 모바일 환경에서의 안정성을 결정합니다.

<br>

에셋의 메모리 생명주기를 직접 제어하는 AssetBundle과 Addressables의 로드/해제 패턴은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서, Unity 엔진의 기본 구조와 실행 흐름은 [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)에서 각각 확인할 수 있습니다.

<br>

---

**관련 글**
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)

**시리즈**
- [Unity 에셋 시스템 (1) - Asset Import Pipeline](/dev/unity/UnityAsset-1/)
- [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)
- **Unity 에셋 시스템 (3) - Scene Management (현재 글)**

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
- [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱](/dev/unity/RasterPipeline-3/)
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)
- [Unity 엔진 핵심 (3) - Unity 실행 순서](/dev/unity/UnityCore-3/)
- [Unity 엔진 핵심 (4) - Unity의 스레딩 모델](/dev/unity/UnityCore-4/)
- [Unity 에셋 시스템 (1) - Asset Import Pipeline](/dev/unity/UnityAsset-1/)
- [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)
- **Unity 에셋 시스템 (3) - Scene Management** (현재 글)
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
