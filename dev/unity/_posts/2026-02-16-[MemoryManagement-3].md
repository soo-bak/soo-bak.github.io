---
layout: single
title: "메모리 관리 (3) - Addressables와 에셋 전략 - soo:bak"
date: "2026-02-16 16:58:00 +0900"
description: AssetBundle의 원리, Addressables 시스템, 로딩 전략, 빌드 사이즈 최적화를 설명합니다.
tags:
  - Unity
  - 최적화
  - Addressables
  - 에셋번들
  - 모바일
---

## 에셋을 필요할 때 불러오는 방법

[메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 확인한 것처럼, 텍스처·메쉬·오디오 클립 같은 에셋은 C# 관리 힙의 래퍼 객체를 통해 접근하지만, 실제 데이터는 네이티브 메모리에 상주합니다.

이전 글에서 함께 살펴본 것처럼, `Resources` 폴더에 넣은 에셋은 사용 여부와 관계없이 빌드에 전부 포함됩니다.
참조 카운팅도 없어서 어떤 에셋이 아직 사용 중인지 추적할 수 없고, 프로젝트가 커질수록 메모리, 빌드 크기, 해제 안전성 모두에서 한계가 드러납니다.

RPG의 수백 종 장비, 오픈 월드의 지역별 환경 에셋, 라이브 서비스의 시즌 콘텐츠처럼 에셋이 계속 늘어나는 프로젝트에서 전부 빌드에 포함하면, 메모리와 초기 다운로드 크기를 감당할 수 없습니다.

**AssetBundle**은 에셋을 빌드와 분리된 별도 파일로 묶어, 필요할 때 로드하고 불필요해지면 해제할 수 있게 합니다. **Addressables**는 이 AssetBundle 위에서 의존성 관리와 참조 카운팅을 자동화하는 추상화 계층입니다.

이 글에서는 두 시스템의 구조를 살펴본 뒤, 로딩 전략, 에셋 중복 감지, 빌드 사이즈 최적화, 번들 그룹 설계까지 다룹니다.

<br>

---

## AssetBundle의 기본 구조

**에셋번들(AssetBundle)**은 Unity 에셋을 별도의 파일로 묶어 빌드하는 시스템입니다.
앱과 별도로 빌드·배포되므로, 앱을 다시 빌드하지 않고도 에셋만 갱신할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text x="270" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">AssetBundle의 기본 구조</text>

  <!-- === 앱 빌드 영역 === -->
  <text x="30" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">앱 빌드 (APK / IPA)</text>
  <rect x="30" y="60" width="220" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">실행 코드</text>
  <text x="140" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">기본 씬 데이터</text>
  <text x="140" y="118" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">StreamingAssets (선택)</text>

  <!-- 분리 표시 -->
  <line x1="270" y1="75" x2="270" y2="135" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <text x="400" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">별도 빌드 · 별도 배포</text>

  <!-- === AssetBundle 파일들 === -->
  <text x="30" y="175" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">AssetBundle 파일들</text>

  <!-- 스테이지 1 번들 -->
  <rect x="30" y="185" width="480" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="206" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스테이지 1</text>
  <rect x="150" y="193" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="195" y="208" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">캐릭터 모델</text>
  <rect x="250" y="193" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="295" y="208" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">환경 텍스처</text>
  <rect x="350" y="193" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="395" y="208" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">배경 음악</text>
  <text x="45" y="228" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">번들</text>
  <text x="150" y="228" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">포함 에셋</text>

  <!-- 스테이지 2 번들 -->
  <rect x="30" y="245" width="480" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="266" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스테이지 2</text>
  <rect x="150" y="253" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="195" y="268" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">보스 모델</text>
  <rect x="250" y="253" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="295" y="268" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">환경 텍스처</text>
  <rect x="350" y="253" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="395" y="268" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">컷씬 데이터</text>

  <!-- 공유 번들 -->
  <rect x="30" y="305" width="480" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="326" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">공유</text>
  <rect x="150" y="313" width="70" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="185" y="328" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">공통 UI</text>
  <rect x="230" y="313" width="55" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="257" y="328" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">폰트</text>
  <rect x="295" y="313" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="328" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">공통 셰이더</text>

  <!-- 배치 위치 안내 -->
  <line x1="100" y1="370" x2="440" y2="370" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <text x="270" y="395" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">로컬 저장소 또는 원격 서버에 배치</text>
</svg>
</div>

AssetBundle의 동작 방식은 빌드, 로드, 언로드의 세 단계로 나뉩니다.

**빌드.**
Unity 에디터에서 에셋을 번들 단위로 묶어 파일을 생성합니다.
각 번들은 독립적인 바이너리 파일이며, 내부에 에셋 데이터와 메타데이터가 압축되어 저장됩니다.

**로드.**
번들 파일이 로컬에 있으면 디스크에서 바로, 원격 서버에 있으면 다운로드 후 캐시를 거쳐 메모리에 올립니다. 메모리에 올린 번들에서 필요한 에셋을 개별적으로 꺼내 사용합니다. 로컬 번들은 보통 **StreamingAssets** 폴더에 넣어 둡니다.

> **StreamingAssets**: Resources, AssetBundle, Addressables는 에셋의 로드·언로드를 다루는 **메모리 관리** 시스템입니다. StreamingAssets는 이와 달리, Unity가 변환하지 말아야 할 원본 파일을 빌드에 포함하기 위한 **파일 저장소**입니다. 이름 그대로 영상·오디오의 스트리밍 재생이 초기 주요 용도였습니다. 당시 영상 플레이어는 Unity 에셋 참조가 아니라 파일 경로로 원본 파일에 직접 접근해야 했는데, Unity의 에셋 파이프라인을 거치면 원본 포맷이 변환되어 이 방식이 불가능했기 때문입니다.
>
> Unity는 일반 에셋을 임포트할 때 플랫폼별 포맷으로 변환하지만, StreamingAssets의 파일은 변환 없이 원본 그대로 빌드에 복사됩니다. Unity의 에셋 시스템에 등록되지 않는 raw 파일이므로, 씬 참조나 Inspector에서 직접 할당할 수 없고 런타임에서 `Application.streamingAssetsPath`를 통해 파일 경로로만 접근합니다. 앱 설치 파일(APK/IPA) 안에 포함되는 폴더이므로 읽기 전용입니다.
>
> AssetBundle(LZ4/LZMA), 영상(H.264) 등 이미 자체 압축이 적용된 파일을 넣는 것이므로, "변환 없음"이 "비압축"을 뜻하지는 않습니다. 파일은 디스크에만 존재하며 명시적으로 로드할 때만 메모리를 사용하므로, 영향을 주는 것은 런타임 메모리가 아니라 앱 설치 크기입니다. 초기 플레이에 필요한 AssetBundle 파일, 스트리밍 재생용 영상, 사전 구축된 데이터베이스(SQLite 등) 등을 넣어 두는 용도로 사용합니다.

**언로드.**
번들이 더 이상 필요 없으면 개발자가 `AssetBundle.Unload()`를 호출하여 메모리에서 해제합니다.

`Unload(true)`는 번들 자체와 그 번들에서 로드한 에셋을 모두 해제합니다.
아직 사용 중인 에셋까지 해제되므로, 텍스처 누락 같은 시각적 결함이 발생할 수 있습니다.

`Unload(false)`는 이 위험을 피하기 위해 번들만 해제하고, 이미 로드한 에셋은 메모리에 남겨둡니다.
다만 에셋이 번들과 분리되어 메모리에 남으므로, 나중에 같은 에셋을 다시 로드하면 중복 복사본이 생길 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Unload(true) vs Unload(false)</text>

  <!-- === Initial State === -->
  <rect x="105" y="32" width="350" height="45" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">메모리: 번들 + 에셋 A + 에셋 B 로드됨</text>
  <text x="280" y="68" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">에셋 A는 화면에 표시 중</text>

  <!-- T-junction split -->
  <line x1="280" y1="77" x2="280" y2="95" stroke="currentColor" stroke-width="1.2"/>
  <line x1="140" y1="95" x2="420" y2="95" stroke="currentColor" stroke-width="1.2"/>
  <line x1="140" y1="95" x2="140" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="136,118 140,126 144,118" fill="currentColor"/>
  <line x1="420" y1="95" x2="420" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="416,118 420,126 424,118" fill="currentColor"/>

  <!-- === Left: Unload(true) === -->
  <text x="140" y="142" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Unload(true)</text>

  <rect x="30" y="152" width="220" height="45" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="140" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">번들 + 모든 에셋 해제</text>
  <text x="140" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.3">(메모리 비어있음)</text>

  <text x="140" y="216" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">에셋 A를 참조하던 오브젝트</text>
  <text x="140" y="232" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">→ 텍스처 누락</text>

  <!-- === Right: Unload(false) === -->
  <text x="420" y="142" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Unload(false)</text>

  <rect x="310" y="152" width="220" height="45" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="420" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">번들만 해제, 에셋 A·B 잔존</text>
  <text x="420" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">번들과의 연결이 끊긴 고아 상태</text>

  <!-- Right: arrow down to reload -->
  <line x1="420" y1="197" x2="420" y2="222" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="416,222 420,230 424,222" fill="currentColor"/>
  <text x="420" y="247" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">같은 번들을 다시 로드하면</text>

  <rect x="310" y="257" width="220" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="420" y="275" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">에셋 A + 에셋 B + 에셋 A'</text>
  <text x="420" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">→ 에셋 A 메모리 중복</text>
</svg>
</div>

<br>

---

## AssetBundle 의존성

Unity의 에셋은 다른 에셋을 참조합니다. 머티리얼은 텍스처를 참조하고, 프리팹은 메쉬와 머티리얼을 참조합니다.
같은 번들 안에서는 이 참조가 자연스럽게 해결되지만, 참조 대상이 다른 번들에 있으면 **번들 간 의존성(Dependency)**이 생깁니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text x="270" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">번들 간 의존성</text>

  <!-- === Bundle A === -->
  <rect x="30" y="45" width="200" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="65" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle A (캐릭터)</text>

  <!-- 캐릭터 프리팹 -->
  <rect x="65" y="80" width="130" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="99" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">캐릭터 프리팹</text>

  <!-- Arrow: 프리팹 → 머티리얼 -->
  <line x1="130" y1="108" x2="130" y2="128" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="126,128 130,136 134,128" fill="currentColor"/>

  <!-- 머티리얼 -->
  <rect x="65" y="138" width="130" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="157" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼</text>

  <!-- === Bundle B === -->
  <rect x="310" y="45" width="200" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="410" y="65" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle B (텍스처)</text>

  <!-- 캐릭터 텍스처 -->
  <rect x="345" y="105" width="130" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">캐릭터 텍스처</text>

  <!-- 번들 경계를 넘는 참조 화살표: 머티리얼 → 텍스처 -->
  <line x1="195" y1="152" x2="340" y2="119" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <polygon points="337,114 345,117 339,122" fill="currentColor"/>
  <text x="270" y="127" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">참조</text>

  <!-- === Bundle A만 로드한 경우 === -->
  <line x1="30" y1="220" x2="510" y2="220" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="30" y="248" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle A만 로드한 경우</text>

  <rect x="40" y="260" width="460" height="22" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <text x="50" y="275" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">1.</text>
  <text x="65" y="275" font-family="sans-serif" font-size="9" fill="currentColor">머티리얼의 텍스처 슬롯이 Bundle B의 에셋을 가리킴</text>

  <rect x="40" y="288" width="460" height="22" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <text x="50" y="303" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">2.</text>
  <text x="65" y="303" font-family="sans-serif" font-size="9" fill="currentColor">Bundle B가 메모리에 없으면 텍스처를 찾을 수 없음</text>

  <rect x="40" y="316" width="460" height="22" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <text x="50" y="331" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">3.</text>
  <text x="65" y="331" font-family="sans-serif" font-size="9" fill="currentColor">화면에 마젠타색 머티리얼이 표시됨</text>

  <!-- === 올바른 로드 순서 === -->
  <line x1="30" y1="355" x2="510" y2="355" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="30" y="383" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">올바른 로드 순서</text>

  <!-- 순서 시각화 -->
  <rect x="40" y="395" width="150" height="28" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="115" y="414" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Bundle B (텍스처)</text>

  <line x1="195" y1="409" x2="240" y2="409" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="240,405 248,409 240,413" fill="currentColor"/>
  <text x="220" y="401" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">먼저</text>

  <rect x="253" y="395" width="150" height="28" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="328" y="414" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Bundle A (캐릭터)</text>
</svg>
</div>

Bundle A의 머티리얼이 Bundle B의 텍스처를 참조하면, Bundle A를 로드하기 전에 Bundle B가 메모리에 있어야 합니다. 의존 번들 없이 로드하면 참조가 끊어져 마젠타색 머티리얼이 표시됩니다.

Bundle A가 Bundle B에, Bundle B가 Bundle C에 의존하면, Bundle A를 로드할 때 B와 C까지 모두 메모리에 있어야 합니다. 번들이 늘어날수록 이 의존 관계를 추적하기 어려워집니다.

Unity는 번들 빌드 시 의존 관계를 **매니페스트(Manifest)**에 자동으로 기록합니다. 하지만 매니페스트를 읽어 로드 순서를 결정하고, 언로드할 때 다른 번들이 아직 참조 중인지 확인하는 일은 개발자가 직접 해야 합니다.
프로젝트 규모가 커지면 이 수동 관리가 오류의 원인이 됩니다.

이 의존성 관리를 자동으로 처리하기 위해 Unity가 제공하는 시스템이 **Addressables**입니다.

---

## Addressables 시스템

Addressables는 AssetBundle 위에 구축된 **추상화 계층(Abstraction Layer)**입니다.
내부적으로 AssetBundle을 그대로 사용하되, 개발자가 직접 해야 했던 번들 지정, 의존성 추적, 해제 시점 판단을 시스템이 대신 처리합니다.

### 주소(Address) 기반 접근

Addressables에서는 각 에셋에 **주소(Address)** 문자열을 부여하고, 개발자가 주소만 지정하면 해당 에셋을 찾아 로드합니다.
에셋이 어떤 번들에 속하는지, 그 번들이 로컬에 있는지 서버에 있는지까지 Addressables가 자동으로 판단합니다.

**AssetBundle 직접 사용 vs Addressables**

| 항목 | AssetBundle 직접 사용 | Addressables |
|---|---|---|
| 로드 절차 | 매니페스트 읽기 → 의존 번들 먼저 로드 → 대상 번들 로드 → 에셋 이름으로 추출 | 주소 하나로 호출 LoadAssetAsync\<T\>("address") |
| 의존성 관리 | 개발자가 직접 추적 | 시스템이 자동 해결 |
| 언로드 | 의존성 역추적 필요 | Release() 호출만으로 처리 |
| 로컬/원격 판별 | 개발자가 경로 지정 | 시스템이 자동 판별 |

<br>

코드로 보면 더 명확합니다.

```csharp
// 텍스처 로드
AsyncOperationHandle<Texture2D> handle =
    Addressables.LoadAssetAsync<Texture2D>("character_diffuse");

handle.Completed += (op) =>
{
    Texture2D texture = op.Result;
    // 텍스처 사용
};

// 사용이 끝나면 해제
Addressables.Release(handle);
```

이 코드에서 개발자가 지정한 것은 `"character_diffuse"`라는 주소뿐이고, 번들 지정, 의존성 해결, 로컬/원격 판별은 Addressables가 내부에서 처리합니다.

<br>

같은 패턴으로 프리팹도 인스턴스화할 수 있습니다.

```csharp
// 프리팹 인스턴스화
AsyncOperationHandle<GameObject> handle =
    Addressables.InstantiateAsync("enemy_prefab");

handle.Completed += (op) =>
{
    GameObject enemy = op.Result;
    // 인스턴스 사용
};

// 사용이 끝나면 해제 (게임오브젝트 파괴 + 참조 카운트 감소)
Addressables.ReleaseInstance(handle.Result);
```

`InstantiateAsync`는 내부적으로 프리팹이 속한 번들을 로드하고, 그 번들이 의존하는 다른 번들도 함께 로드한 뒤, 프리팹을 인스턴스화합니다.

---

### 의존성 자동 해결

Addressables는 빌드 시점에 각 에셋의 주소, 소속 번들, 번들 간 의존성을 **카탈로그(Catalog)** 파일에 기록합니다. 에셋을 로드하면 이 카탈로그를 참조하여 의존 번들을 자동으로 함께 로드합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- Title -->
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">"enemy_prefab" 로드 시 내부 동작</text>

  <!-- Developer call -->
  <rect x="80" y="32" width="300" height="30" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="52" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">LoadAssetAsync("enemy_prefab")</text>

  <!-- Arrow -->
  <line x1="240" y1="62" x2="240" y2="82" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,82 240,90 244,82" fill="currentColor"/>

  <!-- "Addressables 자동 처리" bracket -->
  <line x1="60" y1="94" x2="60" y2="282" stroke="currentColor" stroke-width="1.5" opacity="0.25"/>
  <line x1="60" y1="94" x2="68" y2="94" stroke="currentColor" stroke-width="1.5" opacity="0.25"/>
  <line x1="60" y1="282" x2="68" y2="282" stroke="currentColor" stroke-width="1.5" opacity="0.25"/>
  <text x="40" y="193" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35" transform="rotate(-90, 40, 193)">Addressables 자동 처리</text>

  <!-- Step 1: Catalog lookup -->
  <rect x="80" y="94" width="300" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="92" y="114" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.4">1</text>
  <text x="108" y="114" font-family="sans-serif" font-size="10" fill="currentColor">카탈로그에서 소속 번들과 의존 관계 조회</text>
  <text x="108" y="132" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">→ bundle_prefabs_01 (의존: textures_01, materials_01)</text>

  <!-- Arrow -->
  <line x1="240" y1="142" x2="240" y2="162" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,162 240,170 244,162" fill="currentColor"/>

  <!-- Step 2: Load dependencies -->
  <rect x="80" y="174" width="300" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="92" y="199" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.4">2</text>
  <text x="108" y="192" font-family="sans-serif" font-size="10" fill="currentColor">의존 번들 먼저 로드</text>
  <text x="108" y="209" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">→ bundle_textures_01, bundle_materials_01 → 메모리</text>

  <!-- Arrow -->
  <line x1="240" y1="216" x2="240" y2="236" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,236 240,244 244,236" fill="currentColor"/>

  <!-- Step 3: Load target + extract -->
  <rect x="80" y="248" width="300" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="92" y="273" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.4">3</text>
  <text x="108" y="266" font-family="sans-serif" font-size="10" fill="currentColor">대상 번들 로드 + 에셋 추출</text>
  <text x="108" y="283" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">→ bundle_prefabs_01 → 메모리 → enemy_prefab 추출</text>

  <!-- Arrow -->
  <line x1="240" y1="290" x2="240" y2="306" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,306 240,314 244,306" fill="currentColor"/>

  <!-- Result -->
  <rect x="80" y="318" width="300" height="30" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="338" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">enemy_prefab 반환</text>
</svg>
</div>

개발자가 `"enemy_prefab"`을 로드하면, Addressables는 카탈로그를 조회하여 이 프리팹이 `bundle_prefabs_01`에 속하고, 이 번들이 `bundle_textures_01`과 `bundle_materials_01`에 의존한다는 것을 파악합니다.
그 뒤 의존 번들을 먼저 로드하고, 프리팹이 속한 번들을 로드한 뒤 프리팹을 반환합니다.

이 자동 해결 덕분에, 번들 구조를 재편성하거나 에셋의 번들 소속을 변경해도 기존 로드 코드를 수정할 필요가 없습니다. 
에셋에 부여한 주소 문자열(예: `"character_diffuse"`)만 바꾸지 않으면, 해당 에셋이 어떤 번들로 이동하든 카탈로그 재빌드만으로 반영됩니다.

---

### 참조 카운팅 (Reference Counting)

Addressables는 로드한 에셋에 대해 **참조 카운팅(Reference Counting)**을 적용합니다.

[메모리 관리 (2)](/dev/unity/MemoryManagement-2/)에서 살펴본 것처럼, 참조 카운팅은 특정 자원을 현재 몇 곳에서 사용 중인지 정수로 추적하는 기법입니다. 같은 에셋을 여러 곳에서 로드하면 참조 카운트가 증가하고, `Release()`를 호출하면 감소합니다.

씬에 직접 배치한 에셋은 Unity가 씬 전환 시 자동으로 정리하지만, Addressables로 로드한 에셋은 개발자가 명시적으로 `Release()`를 호출해야 카운트가 감소합니다.

메모리 해제는 개별 에셋이 아니라 번들 단위이므로, 번들에 속한 모든 에셋의 참조 카운트가 0이 되면 Addressables가 언로드 시점을 판단하여 해당 번들을 자동으로 해제합니다. 개발자는 `Release()` 호출까지만 신경 쓰면 됩니다.

<br>

**참조 카운팅 동작 (hero_tex와 hero_mat가 같은 번들에 포함된 경우)**

| 시점 | 동작 | hero_tex | hero_mat | 번들 상태 |
|---|---|---|---|---|
| T1 | LoadAssetAsync("hero_tex") | 1 | - | 번들 로드됨 |
| T2 | LoadAssetAsync("hero_tex") | 2 | - | 유지 (재로드 없음) |
| T3 | LoadAssetAsync("hero_mat") | 2 | 1 | 유지 |
| T4 | Release(hero_tex) 2회 호출 | 0 | 1 | 유지 (hero_mat 사용 중) |
| T5 | Release(hero_mat) | 0 | 0 | 번들 언로드됨 |

T2: 같은 에셋을 다시 로드해도 참조 카운트만 증가, 재로드 없음
T4: hero_tex가 모두 해제되어도 같은 번들의 hero_mat가 사용 중이므로 번들 유지
T5: 번들 내 모든 에셋의 참조 카운트가 0 → 번들이 메모리에서 해제됨

<br>

의존 번들도 참조 카운트로 관리됩니다.
Bundle A의 프리팹이 Bundle B의 텍스처를 참조하고 있다면, 프리팹이 메모리에 있는 한 텍스처도 메모리에 있어야 합니다.
Addressables는 Bundle A를 로드할 때 Bundle B의 참조 카운트도 함께 증가시키므로, Bundle A의 모든 에셋이 해제되어야 Bundle B도 언로드됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">의존 번들의 연쇄 언로드</text>

  <!-- === 의존 관계 === -->
  <!-- Bundle A -->
  <rect x="30" y="45" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="70" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle A (프리팹)</text>

  <!-- 의존 화살표 -->
  <line x1="230" y1="65" x2="320" y2="65" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="320,61 328,65 320,69" fill="currentColor"/>
  <text x="275" y="57" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">의존</text>

  <!-- Bundle B -->
  <rect x="330" y="45" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="70" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle B (텍스처)</text>

  <!-- === 현재 상태 섹션 === -->
  <line x1="20" y1="105" x2="540" y2="105" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="280" y="130" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">현재 상태</text>

  <!-- 에셋 X -->
  <rect x="30" y="145" width="240" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="163" font-family="sans-serif" font-size="10" fill="currentColor">에셋 X (Bundle A)</text>
  <rect x="190" y="151" width="70" height="22" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="225" y="166" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">참조: 2</text>

  <!-- 에셋 Y -->
  <rect x="30" y="191" width="240" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="214" font-family="sans-serif" font-size="10" fill="currentColor">에셋 Y (Bundle A)</text>
  <rect x="190" y="198" width="70" height="22" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="225" y="213" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">참조: 0</text>

  <!-- 상태 결과 -->
  <line x1="280" y1="155" x2="310" y2="155" stroke="currentColor" stroke-width="1"/>
  <polygon points="310,151 318,155 310,159" fill="currentColor"/>
  <text x="430" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Bundle A 유지 → Bundle B도 유지</text>

  <!-- === Release 후 섹션 === -->
  <line x1="20" y1="248" x2="540" y2="248" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="280" y="273" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">에셋 X를 Release하여 참조 카운트 0</text>

  <!-- Step 1: Bundle A 모든 에셋 참조 0 -->
  <rect x="30" y="290" width="240" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="310" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Bundle A의 모든 에셋</text>
  <text x="150" y="328" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">참조 카운트 0</text>

  <!-- Arrow -->
  <line x1="270" y1="315" x2="310" y2="315" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="310,311 318,315 310,319" fill="currentColor"/>

  <!-- Step 2: Bundle A 언로드 -->
  <rect x="325" y="290" width="200" height="50" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="425" y="310" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Bundle A</text>
  <text x="425" y="328" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.6">언로드</text>

  <!-- Arrow down -->
  <line x1="425" y1="340" x2="425" y2="370" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="421,370 425,378 429,370" fill="currentColor"/>

  <!-- Step 3: Bundle B 판정 -->
  <rect x="275" y="385" width="250" height="50" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="400" y="405" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Bundle B를 참조하는 다른 번들 없음</text>
  <text x="400" y="423" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.6">→ Bundle B도 언로드</text>
</svg>
</div>

참조 카운팅은 메모리 관리를 자동화하지만, **`Release()` 호출을 빠뜨리면 메모리 누수가 발생합니다.**

`LoadAssetAsync`를 3번 호출했으면 `Release`도 정확히 3번 호출해야 합니다. 하나라도 빠뜨리면 참조 카운트가 0에 도달하지 못하고, 실제로는 사용하지 않는 에셋이 메모리에 계속 누적됩니다.

`InstantiateAsync`로 생성한 인스턴스도 마찬가지로, `Addressables.ReleaseInstance()`로 해제해야 합니다. `Destroy()`는 Unity 엔진 레벨의 함수여서 게임오브젝트는 파괴하지만, Addressables의 참조 카운트는 감소시키지 않습니다.
원본 에셋과 번들은 메모리에 남게 됩니다.

<br>

**InstantiateAsync로 생성한 오브젝트의 해제 비교**

| 해제 방식 | 오브젝트 | 참조 카운트 | 결과 |
|---|---|---|---|
| Destroy(obj) | 파괴됨 | 유지(감소 안 됨) | 번들 잔류 → 누수 |
| Addressables.ReleaseInstance(obj) | 파괴됨 | 감소 | 카운트 0이면 번들 언로드 |

<br>

씬 전환 시에도 같은 문제가 발생합니다.
`LoadSceneMode.Single`로 새 씬을 로드하면 Unity가 이전 씬의 게임오브젝트를 파괴하고, 내부적으로 `Resources.UnloadUnusedAssets()`를 호출합니다.

하지만 Addressables의 참조 카운트는 그대로 남습니다. Addressables가 참조 카운트 기준으로 "사용 중"이라고 판단하는 에셋은 해제 대상에서 제외되기 때문입니다.

따라서 씬 전환 전에 모든 Addressables 핸들을 명시적으로 `Release()`해야 합니다.

<br>

프로젝트 규모가 커지면 수십 개의 스크립트가 각각 에셋을 로드하고 해제하므로, 어느 스크립트에서 `Release()`가 누락되었는지 코드만으로 파악하기 어렵습니다.
Addressables의 **Event Viewer**(Window > Asset Management > Addressables > Event Viewer)를 사용하면 현재 로드된 에셋과 참조 카운트를 실시간으로 확인할 수 있습니다. 씬 전환이나 특정 이벤트 후에도 참조 카운트가 감소하지 않는 에셋이 있다면 `Release()` 호출이 누락된 것입니다.

<br>

---

## 로딩 전략

Addressables는 의존성 해결과 번들 언로드 시점을 자동으로 처리하지만, 에셋을 **언제** 로드하고 `Release()`할지는 개발자가 결정해야 합니다.

대표적인 접근으로, 씬 진입 전에 필요한 에셋을 모두 올려두는 **프리로드(Preload)**와 실제로 필요해지는 순간에 로드하는 **지연 로드(Lazy Load)**가 있습니다.
프리로드는 게임플레이 중 지연이 없지만 메모리를 오래 점유하고, 지연 로드는 메모리 효율이 높은 대신 로드 지연이 발생할 수 있어서, 실제 게임에서는 두 방식을 상황에 따라 조합합니다.

<br>

---

### 프리로드 (Preload)

앞에서 다룬 것처럼 프리로드는 씬에 필요한 에셋을 미리 올려두는 방식으로, 씬 전환 사이의 로딩 화면에서 이루어집니다. 로딩 화면이 표시되는 동안 게임은 캐릭터 모델, 환경 텍스처, 사운드 등을 메모리에 올립니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프리로드 흐름</text>

  <!-- === 3-stage flow === -->
  <!-- Stage 1: 타이틀 화면 -->
  <rect x="30" y="48" width="130" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="73" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">타이틀 화면</text>

  <!-- Arrow 1→2 -->
  <line x1="160" y1="68" x2="210" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,64 218,68 210,72" fill="currentColor"/>

  <!-- Stage 2: 로딩 화면 -->
  <rect x="220" y="42" width="170" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="305" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">로딩 화면</text>
  <text x="305" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">진행률 표시</text>

  <!-- Arrow 2→3 -->
  <line x1="390" y1="68" x2="440" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="440,64 448,68 440,72" fill="currentColor"/>

  <!-- Stage 3: 게임플레이 씬 -->
  <rect x="450" y="42" width="150" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">게임플레이 씬</text>
  <text x="525" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">지연 없이 즉시 사용</text>

  <!-- === 로딩 화면에서의 로드 항목 === -->
  <line x1="305" y1="94" x2="305" y2="112" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <rect x="235" y="114" width="140" height="62" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="305" y="133" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">캐릭터 로드</text>
  <text x="305" y="149" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">환경 로드</text>
  <text x="305" y="165" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">사운드 로드</text>

  <!-- === 메모리 바 섹션 === -->
  <line x1="30" y1="200" x2="590" y2="200" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="310" y="222" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">메모리</text>

  <!-- Row 1: 타이틀 화면 -->
  <text x="30" y="254" font-family="sans-serif" font-size="10" fill="currentColor">타이틀 화면</text>
  <rect x="130" y="240" width="100" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="255" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">기본 에셋</text>

  <!-- Row 2: 로딩 화면 -->
  <text x="30" y="290" font-family="sans-serif" font-size="10" fill="currentColor">로딩 화면</text>
  <rect x="130" y="276" width="100" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="291" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">기본 에셋</text>
  <rect x="232" y="276" width="70" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="267" y="291" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">캐릭터</text>
  <rect x="304" y="276" width="55" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="331" y="291" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">환경</text>
  <rect x="361" y="276" width="65" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="393" y="291" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">사운드</text>
  <text x="440" y="291" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">← 증가</text>

  <!-- Row 3: 게임플레이 -->
  <text x="30" y="326" font-family="sans-serif" font-size="10" fill="currentColor">게임플레이</text>
  <rect x="130" y="312" width="100" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="327" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">기본 에셋</text>
  <rect x="232" y="312" width="70" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="267" y="327" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">캐릭터</text>
  <rect x="304" y="312" width="55" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="331" y="327" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">환경</text>
  <rect x="361" y="312" width="65" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="393" y="327" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">사운드</text>
  <text x="440" y="327" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">← 유지</text>
</svg>
</div>

이렇게 로딩 화면에서 에셋을 미리 올려두면, 게임플레이 중 적을 스폰하거나 이펙트를 재생할 때 디스크 접근 없이 즉시 사용할 수 있습니다.
프레임 단위의 반응이 중요한 액션 게임에서 에셋 로딩으로 인한 끊김은 치명적이기 때문에, 핵심 에셋은 프리로드하는 것이 일반적입니다.

다만, 스테이지 전체에서 사용할 에셋을 한꺼번에 올리면 메모리 점유 시간이 길어집니다.
예를 들어, 스테이지 후반에만 등장하는 보스 에셋도 시작부터 메모리를 차지합니다. 모바일 기기는 일반적으로 RAM이 4~8GB 수준이고 OS와 백그라운드 앱이 상당 부분을 사용하므로, 게임이 쓸 수 있는 메모리는 제한적이며 이 점유가 부담이 됩니다.

이 부담을 줄이기 위해, 에셋을 구역(zone) 또는 단계(phase)별로 분류하여 해당 구간에 필요한 에셋만 로드할 수 있습니다.
한 구역에서 다음 구역으로 이동할 때 이전 구역의 에셋을 해제하고 새 구역의 에셋을 로드하면, 전체 스테이지의 에셋을 동시에 점유하지 않으면서도 게임플레이 중 로딩 지연을 피할 수 있습니다.

<br>

---

### 지연 로드 (Lazy Load)

지연 로드는 에셋이 실제로 필요한 시점에 로드하는 방식입니다. 게임이 적을 스폰할 때 적의 프리팹을 로드하고, 플레이어가 새로운 지역에 진입할 때 해당 지역의 텍스처를 로드합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <!-- Title -->
  <text x="340" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">지연 로드 흐름</text>

  <!-- === 5-stage flow (top row) === -->
  <!-- Stage 1: 게임플레이 중 -->
  <rect x="15" y="48" width="100" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="73" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">게임플레이 중</text>

  <!-- Arrow 1→2 -->
  <line x1="115" y1="68" x2="140" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="140,64 148,68 140,72" fill="currentColor"/>

  <!-- Stage 2: 적 스폰 요청 -->
  <rect x="150" y="42" width="100" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="64" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">적 스폰 요청</text>
  <text x="200" y="82" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.5">LoadAssetAsync</text>

  <!-- Arrow 2→3 -->
  <line x1="250" y1="68" x2="275" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,64 283,68 275,72" fill="currentColor"/>

  <!-- Stage 3: 비동기 로드 + 생성 -->
  <rect x="285" y="42" width="120" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="345" y="64" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">비동기 로드</text>
  <text x="345" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">+ 생성</text>

  <!-- Arrow 3→4 -->
  <line x1="405" y1="68" x2="430" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="430,64 438,68 430,72" fill="currentColor"/>

  <!-- Stage 4: 사용 -->
  <rect x="440" y="48" width="65" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="472" y="73" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">사용</text>

  <!-- Arrow 4→5 -->
  <line x1="505" y1="68" x2="530" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="530,64 538,68 530,72" fill="currentColor"/>

  <!-- Stage 5: Release + 언로드 -->
  <rect x="540" y="42" width="120" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="600" y="64" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Release</text>
  <text x="600" y="82" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.5">Release(handle)</text>

  <!-- API annotation -->
  <text x="200" y="110" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.4">LoadAssetAsync("orc_prefab")</text>
  <text x="600" y="110" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.4">→ 번들 언로드</text>

  <!-- === 메모리 바 섹션 === -->
  <line x1="15" y1="135" x2="660" y2="135" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="340" y="158" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">메모리</text>

  <!-- Row 1: 게임플레이 -->
  <text x="15" y="192" font-family="sans-serif" font-size="10" fill="currentColor">게임플레이</text>
  <rect x="120" y="178" width="100" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="170" y="193" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">기본 에셋</text>

  <!-- Row 2: 적 스폰 -->
  <text x="15" y="228" font-family="sans-serif" font-size="10" fill="currentColor">적 스폰</text>
  <rect x="120" y="214" width="100" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="170" y="229" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">기본 에셋</text>
  <rect x="222" y="214" width="150" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="297" y="229" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">orc + 의존 에셋</text>
  <text x="386" y="229" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">← 증가</text>

  <!-- Row 3: 적 처치 -->
  <text x="15" y="264" font-family="sans-serif" font-size="10" fill="currentColor">적 처치</text>
  <rect x="120" y="250" width="100" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="170" y="265" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">기본 에셋</text>
  <text x="234" y="265" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">← 감소</text>
</svg>
</div>

지연 로드 방식은 에셋이 필요한 시점에만 메모리에 올리고 사용이 끝나면 해제하므로, 특정 시점에 메모리에 올라가 있는 에셋의 양이 줄어들어 전체 메모리 피크가 낮아집니다. 콘텐츠가 방대하여 모든 에셋을 한 번에 올릴 수 없는 오픈 월드 게임에서는 사실상 필수적인 전략입니다.

다만, 에셋을 디스크에서 읽고 압축을 해제해야 하므로 로딩 지연이 발생합니다. 모바일 기기의 저장 장치에서 수 MB 크기의 번들을 읽는 데 수십에서 수백 밀리초가 소요될 수 있으며, 그 동안 해당 에셋은 사용할 수 없습니다.

이 지연을 완화하기 위해 Addressables의 `LoadAssetAsync`는 비동기로 동작합니다.
에셋 로드가 진행되는 동안에도 메인 스레드가 블록되지 않아 게임 루프는 계속 실행되므로, 로드 시간이 길어도 화면이 멈추지는 않습니다.

다만 에셋이 준비될 때까지 해당 에셋을 사용하는 기능은 작동할 수 없어서, 개발자는 로드 완료 전에는 대체 오브젝트를 표시하고 완료 후 교체하는 등 에셋 준비 상태에 따른 처리를 구현해야 합니다.

<br>

---

### 프리로드와 지연 로드의 조합

프리로드는 메모리를 오래 점유하고 지연 로드는 로딩 지연이 발생하므로, 실제 프로젝트에서는 에셋의 성격에 따라 두 전략을 나누어 적용합니다.

**혼합 전략 예시**

| 전략 | 에셋 예시 | 이유 |
|---|---|---|
| 프리로드 (로딩 화면) | 플레이어 캐릭터 모델, 애니메이션, 기본 환경 텍스처, 공통 UI, 기본 사운드 | 없으면 게임 진행 불가, 즉시 사용 가능해야 함 |
| 지연 로드 (필요 시점) | NPC 모델 (해당 지역 진입 시), 보스 에셋, 이벤트 컷씬, 수집 아이템 | 필요할 때만 메모리 사용, 약간의 로딩 지연 허용 |

이 분류는 프로젝트마다 달라지지만, 기준은 로딩 지연이 플레이어 경험을 해치는지 여부입니다.

<br>

---

## 에셋 중복과 Analyze 도구

로딩 전략이 효과를 발휘하려면 번들 구조 자체가 효율적이어야 합니다.
번들 구조를 잘못 설계하면 동일한 에셋이 여러 번들에 복사되는 **에셋 중복(Asset Duplication)**이 발생하는데, 이렇게 중복된 에셋은 빌드 크기를 불필요하게 늘리고 런타임에서도 동일한 데이터가 메모리에 여러 번 로드될 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">에셋 중복 발생 조건</text>
  <!-- Bundle A box (top-left) -->
  <rect x="50" y="40" width="170" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="135" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle A</text>
  <text x="135" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 A</text>
  <!-- Bundle B box (top-right) -->
  <rect x="300" y="40" width="170" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="385" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle B</text>
  <text x="385" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 B</text>
  <!-- Arrow from Bundle A down to shared texture -->
  <line x1="135" y1="110" x2="215" y2="155" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,155 207,152 210,145" fill="currentColor"/>
  <!-- Arrow from Bundle B down to shared texture -->
  <line x1="385" y1="110" x2="305" y2="155" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="305,155 310,145 313,152" fill="currentColor"/>
  <!-- "참조" labels on arrows -->
  <text x="163" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">참조</text>
  <text x="357" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">참조</text>
  <!-- Shared texture (unassigned, dashed border) -->
  <rect x="170" y="155" width="180" height="35" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="260" y="177" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">공유 텍스처 (미할당)</text>
  <!-- Divider -->
  <line x1="50" y1="215" x2="470" y2="215" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="260" y="237" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">빌드 결과</text>
  <!-- Bundle A result box (bottom-left) -->
  <rect x="50" y="250" width="170" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="135" y="270" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle A</text>
  <text x="135" y="293" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 A</text>
  <text x="135" y="313" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">텍스처 사본</text>
  <text x="135" y="337" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">2 MB</text>
  <!-- Bundle B result box (bottom-right) -->
  <rect x="300" y="250" width="170" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="385" y="270" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle B</text>
  <text x="385" y="293" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 B</text>
  <text x="385" y="313" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">텍스처 사본</text>
  <text x="385" y="337" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">2 MB</text>
  <!-- "동일 텍스처가 복사됨" annotation -->
  <text x="260" y="313" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">← 동일 텍스처가 복사됨 →</text>
  <!-- Bottom summary -->
  <text x="260" y="380" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스처 크기가 2 MB라면, 총 4 MB 사용</text>
  <text x="260" y="400" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">(2 MB 낭비)</text>
</svg>
</div>

Addressables에서 에셋을 그룹에 넣으면 해당 그룹의 번들에 포함되므로, 다른 번들의 에셋이 이 에셋을 참조하더라도 빌드 시스템은 복사하지 않고 번들 간 의존성만 생성합니다.
그런데 참조되는 에셋이 어떤 그룹에도 할당되지 않으면 가리킬 번들이 없으므로, 빌드 시스템은 참조하는 번들 각각에 복사본을 포함시킵니다.
위 다이어그램에서 공유 텍스처가 미할당 상태이기 때문에 Bundle A와 B 양쪽에 사본이 들어간 것입니다.

공유 텍스처를 `Bundle_Shared`처럼 별도 그룹에 할당하면, Bundle A와 B에는 복사본 대신 의존성만 남습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- Title -->
  <text x="230" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">중복 해결: 공유 번들 분리</text>
  <!-- Bundle A box -->
  <rect x="40" y="40" width="150" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="115" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle A</text>
  <text x="115" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 A</text>
  <!-- Bundle B box -->
  <rect x="270" y="40" width="150" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="345" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle B</text>
  <text x="345" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 B</text>
  <!-- Arrow from Bundle A down -->
  <line x1="115" y1="110" x2="195" y2="155" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,155 187,152 190,145" fill="currentColor"/>
  <!-- Arrow from Bundle B down -->
  <line x1="345" y1="110" x2="265" y2="155" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="265,155 270,145 273,152" fill="currentColor"/>
  <!-- "의존" labels on arrows -->
  <text x="143" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">의존</text>
  <text x="317" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">의존</text>
  <!-- Bundle_Shared box -->
  <rect x="140" y="155" width="180" height="75" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="178" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bundle_Shared</text>
  <text x="230" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">공유 텍스처</text>
  <text x="230" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">← 한 번만 존재</text>
  <!-- Bottom summary -->
  <text x="230" y="260" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스처 크기 2 MB × 1 = 2 MB</text>
  <text x="230" y="280" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">(중복 없음)</text>
</svg>
</div>

공유 에셋을 별도 그룹에 할당하면 중복은 해결되지만, 에셋이 수백, 수천 개인 프로젝트에서는 어떤 에셋이 중복되었는지 수동으로 찾기 어려운데, Addressables에 내장된 **Analyze 도구**(에디터에서 Window > Asset Management > Addressables > Analyze)가 이 검출을 자동으로 수행합니다.

Analyze 도구의 "Check Duplicate Bundle Dependencies" 규칙을 실행하면 여러 번들에 중복 포함된 에셋 목록과 각 에셋이 어떤 번들에 포함되어 있는지 표시되고, "Fix Selected Rules"를 누르면 중복 에셋을 별도 그룹으로 자동 분리합니다.

<br>

---

## 빌드 사이즈 최적화

런타임 메모리와 함께 초기 다운로드 크기도 모바일에서 중요합니다. Google Play의 **AAB(Android App Bundle)**는 기본 모듈 크기에 제한이 있어 이를 초과하면 앱을 게시할 수 없고, iOS에서는 일정 크기를 넘으면 셀룰러 다운로드 시 경고가 표시되어 사용자가 설치를 미루거나 포기할 수 있습니다. 이러한 제약 안에서 풍부한 콘텐츠를 제공하려면 에셋 배포 전략이 필요합니다.

<br>

---

### 온디맨드 다운로드

온디맨드 다운로드는 초기 설치에 타이틀 화면, 튜토리얼, 첫 번째 스테이지처럼 필수적인 에셋만 포함하고, 나머지는 게임 진행에 따라 서버에서 받아오는 방식입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">온디맨드 다운로드 구조</text>

  <!-- Initial Install Box -->
  <rect x="30" y="38" width="340" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="56" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">초기 설치 (APK / IPA)</text>
  <text x="50" y="78" font-family="sans-serif" font-size="11" fill="currentColor">실행 코드</text>
  <text x="50" y="96" font-family="sans-serif" font-size="11" fill="currentColor">타이틀 / 튜토리얼 에셋</text>
  <text x="50" y="114" font-family="sans-serif" font-size="11" fill="currentColor">Addressables 카탈로그</text>
  <text x="50" y="132" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">≤ 200MB</text>
  <!-- Size badge -->
  <rect x="390" y="68" width="90" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4 2"/>
  <text x="435" y="88" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">≤ 200MB</text>
  <line x1="370" y1="88" x2="390" y2="88" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>

  <!-- Download Arrow between boxes -->
  <line x1="200" y1="138" x2="200" y2="168" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="194,163 200,174 206,163" fill="currentColor"/>
  <text x="215" y="158" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">다운로드</text>

  <!-- CDN Server Box -->
  <rect x="30" y="178" width="340" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="198" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">원격 서버 (CDN)</text>
  <text x="200" y="213" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">전 세계에 분산된 콘텐츠 배포 서버</text>

  <!-- Bundle items -->
  <rect x="55" y="224" width="290" height="22" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <text x="65" y="239" font-family="sans-serif" font-size="10" fill="currentColor">스테이지 1 번들</text>
  <text x="330" y="239" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">50MB</text>

  <rect x="55" y="250" width="290" height="22" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <text x="65" y="265" font-family="sans-serif" font-size="10" fill="currentColor">스테이지 2 번들</text>
  <text x="330" y="265" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">80MB</text>

  <rect x="55" y="276" width="290" height="22" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <text x="65" y="291" font-family="sans-serif" font-size="10" fill="currentColor">스테이지 3 번들</text>
  <text x="330" y="291" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">60MB</text>

  <rect x="55" y="302" width="290" height="22" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <text x="65" y="317" font-family="sans-serif" font-size="10" fill="currentColor">이벤트 콘텐츠 번들</text>
  <text x="330" y="317" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">30MB</text>

  <!-- Divider line -->
  <line x1="30" y1="348" x2="490" y2="348" stroke="currentColor" stroke-width="0.5" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- Game Flow Section -->
  <text x="260" y="375" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">게임 진행 흐름</text>

  <!-- Flow: Tutorial → Stage 1 download → Play -->
  <rect x="30" y="390" width="90" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="409" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">튜토리얼 완료</text>

  <line x1="120" y1="405" x2="148" y2="405" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="143,400 153,405 143,410" fill="currentColor"/>

  <rect x="155" y="390" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="409" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">스테이지 1 다운로드</text>

  <line x1="275" y1="405" x2="303" y2="405" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="298,400 308,405 298,410" fill="currentColor"/>

  <rect x="310" y="390" width="60" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="409" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">플레이</text>

  <!-- Flow: → Stage 2 download → Play -->
  <line x1="340" y1="420" x2="340" y2="438" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <line x1="340" y1="438" x2="215" y2="438" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <line x1="215" y1="438" x2="215" y2="448" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <polygon points="210,444 215,454 220,444" fill="currentColor"/>

  <rect x="155" y="455" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="474" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">스테이지 2 다운로드</text>

  <line x1="275" y1="470" x2="303" y2="470" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="298,465 308,470 298,475" fill="currentColor"/>

  <rect x="310" y="455" width="60" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="474" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">플레이</text>

  <!-- Continuation dots -->
  <text x="215" y="505" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor" opacity="0.5">⋯</text>
</svg>
</div>

Addressables는 번들의 위치를 로컬과 원격으로 구분할 수 있는데, 그룹 설정에서 "Build & Load Path"를 원격(Remote)으로 지정하면 해당 번들은 빌드 후 **CDN(Content Delivery Network)** 등의 원격 서버에 업로드됩니다.
CDN은 전 세계에 분산된 서버 네트워크로 사용자와 가까운 서버에서 파일을 전송하므로 다운로드 속도가 빠릅니다.
런타임에서 해당 번들이 필요하면 원격 서버에서 다운로드하여 기기의 로컬 캐시에 저장하고, 같은 번들을 다시 요청하면 네트워크 통신 없이 캐시에서 로드합니다.

Addressables가 번들의 관리와 로드를 담당한다면, 번들을 기기에 전달하는 경로는 각 플랫폼의 배포 시스템이 담당합니다.
Android의 **PAD(Play Asset Delivery)**는 install-time(앱 설치와 함께), fast-follow(설치 직후 백그라운드), on-demand(앱이 요청할 때) 세 가지 전달 모드를 제공하고, iOS의 **ODR(On-Demand Resources)**는 태그를 부여한 리소스를 앱 요청 시 App Store에서 다운로드합니다.
Addressables는 이러한 플랫폼 배포 시스템과 연동하여, 개발자가 동일한 Addressables API로 에셋을 로드하면서 실제 전달 경로는 플랫폼에 맡길 수 있습니다.

<br>

---

### 에셋 압축 방식

AssetBundle은 빌드 시 압축되는데, 압축 방식에 따라 번들의 파일 크기, 로드 속도, 메모리 사용 패턴이 달라집니다.

**AssetBundle 압축 방식 비교**

| 항목 | LZ4 | LZMA |
|---|---|---|
| 압축률 | 중간 (원본의 약 60~70%) | 높음 (원본의 약 40~50%) |
| 로드 방식 | 청크(Chunk) 단위, 부분 접근 가능 | 전체 압축 해제 후 접근 |
| 로드 속도 | 빠름 (필요한 부분만 해제) | 느림 (전체를 먼저 해제) |
| 메모리 | 낮음 (청크만 해제) | 높음 (전체 해제 버퍼 필요) |
| 용도 | 런타임 로딩용, 모바일 권장 | 다운로드/배포용, 크기 절약 |

**LZ4**는 데이터를 독립적인 블록(chunk)으로 나누어 각각 압축하므로, 번들 내부의 에셋에 접근할 때 해당 에셋이 속한 블록만 압축을 해제합니다.
번들 전체를 한꺼번에 해제하지 않으므로 로드 속도가 빠르고 메모리 피크도 낮아, 모바일에서 런타임 로딩에 적합합니다.

**LZMA**는 데이터를 하나의 연속된 스트림으로 압축하므로 압축률이 높고, 같은 에셋을 LZ4로 압축했을 때보다 파일 크기가 작아 다운로드 크기를 줄이는 데 유리합니다.
대신 에셋 하나에 접근하려면 Unity가 번들 전체를 메모리에 압축 해제해야 하므로, 해제 시간이 길고 임시 버퍼가 필요하여 메모리 피크가 높아집니다.
다만 Unity는 LZMA 번들을 최초 다운로드한 뒤 로컬 캐시에 LZ4로 재압축하여 저장하므로, 이 비용은 첫 다운로드 시에만 발생하고 이후 로드에서는 캐시된 LZ4 버전을 사용합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">LZ4 vs LZMA 메모리 피크 비교</text>

  <!-- ===== LZ4 Section ===== -->
  <text x="30" y="52" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">LZ4 로드 과정</text>

  <!-- LZ4 flow boxes -->
  <rect x="30" y="62" width="90" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="84" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">블록 로드</text>

  <line x1="120" y1="80" x2="148" y2="80" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="143,75 153,80 143,85" fill="currentColor"/>

  <rect x="155" y="62" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="205" y="84" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">블록 압축 해제</text>

  <line x1="255" y1="80" x2="283" y2="80" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="278,75 288,80 278,85" fill="currentColor"/>

  <rect x="290" y="62" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="84" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">최종 에셋</text>

  <!-- LZ4 Memory peak bar (small) -->
  <text x="30" y="120" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">메모리 피크</text>
  <rect x="100" y="110" width="130" height="18" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="165" y="123" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">블록 + 에셋만</text>
  <!-- Peak indicator -->
  <line x1="230" y1="104" x2="230" y2="128" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" opacity="0.4"/>
  <text x="240" y="107" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">낮음</text>

  <!-- Divider -->
  <line x1="20" y1="145" x2="500" y2="145" stroke="currentColor" stroke-width="0.5" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- ===== LZMA Section ===== -->
  <text x="30" y="172" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">LZMA 로드 과정</text>

  <!-- LZMA flow boxes -->
  <rect x="30" y="182" width="90" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">번들 로드</text>

  <line x1="120" y1="200" x2="148" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="143,195 153,200 143,205" fill="currentColor"/>

  <rect x="155" y="182" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="245" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">전체 압축 해제</text>
  <text x="245" y="212" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(번들 + 해제 버퍼 동시 존재)</text>

  <line x1="335" y1="200" x2="363" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="358,195 368,200 358,205" fill="currentColor"/>

  <rect x="370" y="182" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="410" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">최종 에셋</text>

  <!-- LZMA Memory peak bar (large — visually wider to show higher peak) -->
  <text x="30" y="242" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">메모리 피크</text>
  <rect x="100" y="232" width="320" height="18" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="245" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">번들 + 전체 해제 버퍼</text>
  <!-- Peak indicator -->
  <line x1="420" y1="226" x2="420" y2="250" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" opacity="0.4"/>
  <text x="430" y="229" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">높음</text>

  <!-- Comparison bracket -->
  <line x1="460" y1="119" x2="480" y2="119" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="480" y1="119" x2="480" y2="241" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="460" y1="241" x2="480" y2="241" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="492" y="170" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5" writing-mode="tb">피크 차이</text>

  <!-- Scale reference -->
  <text x="260" y="285" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">바 길이 = 상대적 메모리 피크 크기</text>
</svg>
</div>

실제로 원격 배포용 번들은 LZMA로 빌드하여(Addressables 그룹 설정의 Bundle Compression 옵션) 다운로드 크기를 줄이고, 런타임 로드에는 캐시된 LZ4 버전을 활용하는 조합이 일반적입니다.
이 재압축은 `Caching.compressionEnabled` 속성(기본값 `true`)이 제어합니다.

<br>

---

### 비압축(Uncompressed)

비압축 번들은 파일 크기가 가장 크지만 압축 해제 과정이 없으므로 로드 속도가 가장 빠릅니다.

오디오나 비디오처럼 이미 자체 압축(Vorbis, H.264 등)이 적용된 데이터에는 번들 압축이 추가적인 크기 절약을 주지 않으면서 해제 비용만 늘리므로, 비압축이 합리적일 수 있습니다.

<br>

---

## 번들 그룹 전략

압축 방식은 번들의 로드 속도와 메모리 사용을 결정하지만, 압축의 효과를 최대한 활용하려면 어떤 에셋을 어떤 번들에 묶을지를 먼저 설계해야 합니다.
Addressables에서는 **그룹(Group)** 하나가 하나의 번들(또는 설정에 따라 여러 번들)로 빌드되므로, 그룹 구성이 곧 다운로드 크기, 로딩 시간, 메모리 사용량을 결정하며, **함께 사용되는 에셋을 같은 그룹에 묶는 것**이 기본 원칙입니다.

예를 들어 특정 스테이지에서만 사용되는 에셋은 하나의 그룹으로, 여러 스테이지에서 공통으로 사용되는 에셋은 별도의 공유 그룹으로 분리하면, 해당 스테이지에 진입할 때 필요한 번들만 로드하고 다른 스테이지로 전환할 때 해제할 수 있습니다.

모든 에셋을 하나의 번들에 넣으면 에셋 하나를 쓰기 위해 전체를 로드해야 하고, 에셋 하나만 수정해도 전체 번들을 다시 다운로드해야 합니다.
반대로 에셋마다 개별 번들을 만들면 번들 수가 수백 개로 늘어나 카탈로그가 비대해지고 HTTP 요청 수가 증가합니다. 
이 두 극단을 피해 번들 하나의 크기를 5~30MB 정도로 유지하면 로드 시간과 관리 편의성 사이에서 균형을 잡기 쉽습니다.

<br>

콘텐츠 업데이트 빈도도 그룹 분리의 기준이 됩니다.
자주 변경되는 에셋(이벤트 콘텐츠, 시즌 스킨)과 거의 변경되지 않는 에셋(기본 UI, 공통 셰이더)을 같은 그룹에 넣으면 이벤트 콘텐츠만 바뀌어도 전체 번들을 다시 다운로드해야 하므로, 업데이트 빈도가 다른 에셋은 별도 그룹으로 분리합니다.

이렇게 그룹을 분리해 두면 변경된 번들만 선택적으로 업데이트할 수 있습니다.
Addressables는 에셋 주소와 번들 위치를 **카탈로그**에 기록하고, 카탈로그의 내용을 **해시(Hash)** 값으로 요약합니다.
해시는 파일 내용을 고정 길이 문자열로 변환한 값으로, 파일이 한 바이트라도 바뀌면 달라집니다.
서버에 새 번들을 배포하면 카탈로그도 갱신되어 해시가 바뀌는데, 앱이 시작될 때 Addressables가 로컬 해시와 서버 해시를 비교하여 다르면 새 카탈로그를 자동으로 다운로드합니다. 이 덕분에 앱 스토어에 앱을 다시 제출하지 않고도 에셋을 업데이트할 수 있습니다.

<br>

---

## 메모리에서 서브시스템으로

메모리 관리 시리즈에서 가비지 컬렉션의 원리, 네이티브 메모리와 에셋의 구조, Addressables를 통한 에셋 로드/언로드 전략까지 다루었습니다.
스크립트 최적화 시리즈에서 다룬 C# 메모리 할당 패턴까지 합치면 메모리와 스크립트 수준의 최적화 기초를 갖춘 셈입니다.

다음으로는 UI, 라이팅, 셰이더, 물리, 파티클, 애니메이션 등 Unity 개별 서브시스템의 최적화 패턴을 다루며, 그 첫 번째인 UI 최적화 시리즈에서 Canvas, 레이아웃, 배칭의 구조와 모바일 UI 최적화를 살펴봅니다.

<br>

---

## 마무리

모바일 메모리를 최적화하려면 에셋을 세밀하게 관리해야 하며, AssetBundle이 에셋을 별도 파일로 분리하는 기반을 제공하고 Addressables가 그 위에서 의존성 해결과 참조 카운팅을 자동으로 처리합니다.

- AssetBundle은 에셋을 별도 파일로 빌드하여 필요할 때 로드하고, 불필요해지면 언로드하는 구조를 제공합니다
- 에셋의 참조 관계가 번들 경계를 넘으면 번들 간 의존성이 발생하며, 개발자가 이를 수동으로 관리해야 하는 것이 AssetBundle 직접 사용의 한계입니다
- Addressables는 카탈로그를 기반으로 주소 기반 접근, 의존성 자동 해결, 참조 카운팅을 제공하여 번들 관리를 추상화합니다
- 프리로드는 게임플레이 중 지연을 제거하고, 지연 로드는 필요한 시점에만 에셋을 올려 메모리 효율을 높입니다
- `Release()` 호출을 빠뜨리면 참조 카운트가 감소하지 않아, Addressables가 번들을 해제하지 못하고 메모리 누수가 발생합니다
- Analyze 도구의 "Check Duplicate Bundle Dependencies" 규칙으로 에셋 중복을 검출하고, 공유 에셋은 별도 그룹으로 분리합니다
- 모바일 번들은 LZ4 압축이 권장되며, LZMA는 다운로드 크기 절감에 유리합니다
- 초기 설치에는 핵심 에셋만 포함하고, 나머지는 온디맨드 다운로드로 플랫폼별 설치 크기 제한을 지킵니다

번들 구조 설계, 로딩 전략, 압축 방식, 중복 검출은 서로 연결되어 있어서, 그룹을 잘 나눠야 로딩 전략이 효과를 발휘하고 중복이 없어야 압축과 다운로드 최적화가 실질적인 크기 절감으로 이어집니다.
이어지는 [UIOptimization 시리즈](/dev/unity/UIOptimization-1/)에서는 Canvas 시스템의 구조와 모바일 UI 최적화를 다룹니다.

<br>

---

**관련 글**
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)

**시리즈**
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- **메모리 관리 (3) - Addressables와 에셋 전략** (현재 글)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- **메모리 관리 (3) - Addressables와 에셋 전략** (현재 글)
- [UI 최적화 (1) - 캔버스와 리빌드 시스템](/dev/unity/UIOptimization-1/)
- [UI 최적화 (2) - UI 최적화 전략](/dev/unity/UIOptimization-2/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
