---
layout: single
title: "Unity 에셋 시스템 (1) - Asset Import Pipeline - soo:bak"
date: "2026-03-05 23:03:00 +0900"
description: 소스 에셋과 임포트 에셋, Library 폴더, 텍스처·모델·오디오 임포트 과정, Import Settings의 영향을 설명합니다.
tags:
  - Unity
  - 에셋
  - Import
  - Pipeline
  - 모바일
---

## 에셋 시스템을 먼저 이해해야 하는 이유

게임에 쓰이는 이미지와 모델, 사운드는 대부분 Photoshop이나 Maya, Audacity 같은 외부 도구에서 만들어집니다. 그런데 이렇게 만든 원본 파일은 Unity로 가져온다고 해서 그대로 쓰이지 않습니다. Unity는 PSD나 FBX를 런타임에서 직접 읽지 못하므로, 프로젝트에 들어온 원본을 엔진이 다룰 수 있는 데이터로 변환해 둡니다. 이렇게 원본을 엔진용 데이터로 바꾸어 저장하는 전체 과정을 **Asset Import Pipeline**이라고 부릅니다.

이 과정은 단순히 파일 형식을 바꾸는 데 그치지 않습니다. 같은 원본이라도 어떤 설정으로 임포트하느냐에 따라 결과물의 크기와 품질이 달라지고, 빌드 크기와 메모리 사용량, 로딩 속도가 모두 이 단계에서 정해집니다. 특히 에셋이 수백, 수천 개에 이르는 모바일 프로젝트에서는 이런 차이가 쌓여 무시할 수 없는 규모가 됩니다. 따라서 에셋을 최적화하려면 임포트 단계부터 이해해야 합니다.

이 글에서는 먼저 소스 에셋과 임포트 에셋을 구분하고, Library 폴더와 `.meta` 파일의 역할을 정리합니다. 이어서 텍스처와 모델, 오디오의 주요 Import Settings가 빌드 크기와 메모리 사용량에 어떤 영향을 주는지 살펴봅니다.

---

## 소스 에셋 vs 임포트 에셋

Unity는 프로젝트의 에셋을 원본과 변환본, 두 가지로 나누어 다룹니다. 가령 `character.psd`를 프로젝트에 넣으면, 아티스트가 Photoshop에서 열어 수정하는 원본 파일은 **소스 에셋(Source Asset)**이고, Unity가 그 원본을 변환해 런타임에서 사용하는 엔진용 데이터는 **임포트 에셋(Imported Asset)**입니다.

소스 에셋은 제작 도구가 만든 원본 파일입니다. Photoshop의 PSD, Maya나 Blender의 FBX, Audacity의 WAV처럼 제작 단계의 포맷을 유지한 채 `Assets` 폴더에 놓입니다. 아티스트와 사운드 디자이너가 직접 수정하는 대상이므로, Git 같은 버전 관리에 반드시 포함해야 합니다.

임포트 에셋은 이 변환을 거쳐 만들어진 결과물입니다. Unity는 PSD를 ASTC 같은 GPU 압축 텍스처로, FBX를 엔진 내부의 메쉬 포맷으로 바꿉니다. 이렇게 변환된 데이터는 원본과 별개의 파일로 `Library` 폴더에 저장됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="280" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">소스 에셋과 임포트 에셋의 관계</text>
  <!-- Left box -->
  <rect x="10" y="30" width="210" height="190" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="115" y="52" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Assets 폴더 (소스 에셋)</text>
  <line x1="25" y1="60" x2="205" y2="60" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="30" y="82" font-size="11" font-family="sans-serif">character.psd</text>
  <text fill="currentColor" x="30" y="102" font-size="11" font-family="sans-serif">character.fbx</text>
  <text fill="currentColor" x="30" y="122" font-size="11" font-family="sans-serif">bgm.wav</text>
  <text fill="currentColor" x="30" y="142" font-size="11" font-family="sans-serif">icon.png</text>
  <text fill="currentColor" x="30" y="175" font-size="9" font-family="sans-serif" opacity="0.5">※ 버전 관리 대상</text>
  <text fill="currentColor" x="30" y="192" font-size="9" font-family="sans-serif" opacity="0.5">※ 원본 포맷 유지</text>
  <!-- Right box -->
  <rect x="330" y="30" width="220" height="190" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="440" y="52" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Library 폴더 (임포트 에셋)</text>
  <line x1="345" y1="60" x2="535" y2="60" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="350" y="82" font-size="11" font-family="sans-serif">텍스처 (ASTC 압축)</text>
  <text fill="currentColor" x="350" y="102" font-size="11" font-family="sans-serif">메쉬 (Unity 포맷)</text>
  <text fill="currentColor" x="350" y="122" font-size="11" font-family="sans-serif">오디오 (Vorbis 압축)</text>
  <text fill="currentColor" x="350" y="142" font-size="11" font-family="sans-serif">스프라이트 데이터</text>
  <text fill="currentColor" x="350" y="175" font-size="9" font-family="sans-serif" opacity="0.5">※ 버전 관리에서 제외</text>
  <text fill="currentColor" x="350" y="192" font-size="9" font-family="sans-serif" opacity="0.5">※ 플랫폼별 변환 결과</text>
  <!-- Arrow 1 -->
  <line x1="220" y1="78" x2="322" y2="78" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="328,78 320,74 320,82" fill="currentColor"/>
  <text fill="currentColor" x="271" y="73" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">import</text>
  <!-- Arrow 2 -->
  <line x1="220" y1="98" x2="322" y2="98" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="328,98 320,94 320,102" fill="currentColor"/>
  <text fill="currentColor" x="271" y="93" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">import</text>
  <!-- Arrow 3 -->
  <line x1="220" y1="118" x2="322" y2="118" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="328,118 320,114 320,122" fill="currentColor"/>
  <text fill="currentColor" x="271" y="113" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">import</text>
  <!-- Arrow 4 -->
  <line x1="220" y1="138" x2="322" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="328,138 320,134 320,142" fill="currentColor"/>
  <text fill="currentColor" x="271" y="133" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">import</text>
</svg>
</div>

<br>

소스 에셋을 `Assets` 폴더에 추가하면, Unity 에디터가 변경을 감지해 자동으로 임포트합니다. 이 변환을 어떻게 수행할지는 에셋마다 지정되는 **Import Settings**가 정하며, 최종 해상도를 제한하는 Max Size, 압축 포맷, 밉맵 생성 여부 같은 항목이 여기에 담깁니다.

### .meta 파일

Import Settings는 다음 임포트 때도 같은 값이 적용되도록 어딘가에 저장되어야 합니다. 이를 위해 Unity는 소스 에셋마다 짝이 되는 `.meta` 파일을 만들어 둡니다. `character.psd`를 추가하면 그 옆에 `character.psd.meta`가 생깁니다.

`.meta` 파일에는 이 Import Settings뿐 아니라, 그 에셋의 **GUID(Globally Unique Identifier)**도 함께 담깁니다. GUID는 프로젝트 안에서 특정 에셋을 가리키는 고유한 문자열입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="290" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">.meta 파일의 역할</text>

  <!-- Left box: Assets folder -->
  <rect x="10" y="30" width="275" height="230" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="147" y="52" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Assets/ 폴더</text>
  <line x1="25" y1="60" x2="270" y2="60" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Pair 1: character -->
  <text fill="currentColor" x="30" y="82" font-size="10" font-family="monospace">character.psd</text>
  <text fill="currentColor" x="270" y="82" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">소스 에셋</text>
  <rect x="15" y="89" width="265" height="16" rx="2" fill="currentColor" fill-opacity="0.04"/>
  <text fill="currentColor" x="30" y="101" font-size="10" font-family="monospace">character.psd.meta</text>
  <text fill="currentColor" x="270" y="101" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">GUID + Settings</text>

  <!-- Pair 2: enemy -->
  <text fill="currentColor" x="30" y="130" font-size="10" font-family="monospace">enemy.fbx</text>
  <text fill="currentColor" x="270" y="130" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">소스 에셋</text>
  <rect x="15" y="137" width="265" height="16" rx="2" fill="currentColor" fill-opacity="0.04"/>
  <text fill="currentColor" x="30" y="149" font-size="10" font-family="monospace">enemy.fbx.meta</text>
  <text fill="currentColor" x="270" y="149" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">GUID + Settings</text>

  <!-- Pair 3: bgm -->
  <text fill="currentColor" x="30" y="178" font-size="10" font-family="monospace">bgm.wav</text>
  <text fill="currentColor" x="270" y="178" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">소스 에셋</text>
  <rect x="15" y="185" width="265" height="16" rx="2" fill="currentColor" fill-opacity="0.04"/>
  <text fill="currentColor" x="30" y="197" font-size="10" font-family="monospace">bgm.wav.meta</text>
  <text fill="currentColor" x="270" y="197" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">GUID + Settings</text>

  <!-- Notes -->
  <text fill="currentColor" x="30" y="230" font-size="9" font-family="sans-serif" opacity="0.5">※ .meta 파일은 반드시 버전 관리에 포함</text>
  <text fill="currentColor" x="30" y="246" font-size="9" font-family="sans-serif" opacity="0.5">※ 소스 에셋과 항상 쌍으로 존재</text>

  <!-- Arrow from .meta to right box -->
  <line x1="285" y1="98" x2="322" y2="98" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <polygon points="328,98 320,94 320,102" fill="currentColor"/>

  <!-- Right box: .meta content -->
  <rect x="330" y="30" width="240" height="195" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="450" y="52" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">.meta 파일 내용</text>
  <line x1="345" y1="60" x2="555" y2="60" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- GUID -->
  <text fill="currentColor" x="345" y="82" font-size="10" font-family="monospace">guid: a1b2c3d4e5f6...</text>
  <text fill="currentColor" x="555" y="82" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">고유 식별자</text>

  <!-- Separator -->
  <line x1="345" y1="94" x2="555" y2="94" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>

  <!-- Import Settings -->
  <text fill="currentColor" x="345" y="112" font-size="10" font-family="monospace">TextureImporter:</text>
  <text fill="currentColor" x="555" y="112" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">Import Settings</text>
  <text fill="currentColor" x="360" y="132" font-size="10" font-family="monospace" opacity="0.7">maxTextureSize: 1024</text>
  <text fill="currentColor" x="360" y="150" font-size="10" font-family="monospace" opacity="0.7">textureCompression: 2</text>
  <text fill="currentColor" x="360" y="168" font-size="10" font-family="monospace" opacity="0.7">...</text>

  <!-- Right box note -->
  <text fill="currentColor" x="345" y="200" font-size="9" font-family="sans-serif" opacity="0.5">※ Import Settings → 빌드 크기·메모리 결정</text>
</svg>
</div>

<br>

GUID가 중요한 이유는 Unity가 에셋 간 참조를 파일 경로가 아니라 GUID로 저장하기 때문입니다. 예를 들어 머티리얼이 어떤 텍스처를 참조할 때, 내부에는 `"Textures/wall.png"` 같은 경로가 아니라 그 텍스처의 GUID가 저장됩니다. 그래서 파일 이름이나 폴더 위치가 바뀌어도 GUID가 유지되면 머티리얼은 같은 텍스처를 계속 찾을 수 있습니다.

반대로 `.meta` 파일을 지우면 Unity는 해당 에셋에 새 GUID를 부여합니다. 그러면 기존 GUID를 참조하던 머티리얼, 프리팹, 씬의 참조가 끊어집니다. 에셋을 옮기거나 이름을 바꿀 때 Unity 에디터의 Project 창에서 처리해야 하는 것은 이 때문입니다. 에디터는 소스 에셋과 `.meta` 파일을 함께 이동시킵니다.

운영체제의 파일 탐색기에서 파일만 이동하면 소스 에셋과 `.meta` 파일이 분리되어 참조가 깨질 수 있습니다. 따라서 `.meta` 파일은 소스 에셋과 함께 버전 관리에 포함해야 합니다.

---

## Library 폴더: 임포트 캐시

소스 에셋과 `.meta`가 버전 관리에 포함되는 원본이라면, 이를 엔진이 쓸 수 있는 형태로 변환한 결과를 담는 곳이 `Library` 폴더입니다. Unity는 한 번 임포트한 결과를 이 폴더에 기록해 두고 다시 사용하므로, 에디터를 열 때마다 모든 에셋을 새로 변환하지 않아도 됩니다. 이처럼 변환 결과를 모아 두고 재사용하기에 `Library`를 임포트 캐시라고 부릅니다.

<br>

<div style="text-align: center;">
<svg viewBox="0 0 480 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="240" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Library 폴더의 구조</text>

  <!-- Outer box: ProjectRoot -->
  <rect x="10" y="30" width="460" height="270" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="240" y="50" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">ProjectRoot/</text>
  <line x1="25" y1="58" x2="455" y2="58" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Assets/ row -->
  <rect x="25" y="66" width="430" height="24" rx="3" fill="currentColor" fill-opacity="0.05"/>
  <text fill="currentColor" x="35" y="83" font-size="11" font-family="monospace" font-weight="bold">Assets/</text>
  <text fill="currentColor" x="445" y="83" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">소스 에셋 · 버전 관리 O</text>

  <!-- Library/ row + sub-items -->
  <rect x="25" y="98" width="430" height="120" rx="3" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="35" y="117" font-size="11" font-family="monospace" font-weight="bold">Library/</text>
  <text fill="currentColor" x="445" y="117" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">임포트 캐시 · 버전 관리 X</text>

  <!-- Library sub-items -->
  <line x1="55" y1="126" x2="55" y2="200" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- Artifacts/ -->
  <line x1="55" y1="142" x2="70" y2="142" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text fill="currentColor" x="75" y="147" font-size="10" font-family="monospace">Artifacts/</text>
  <text fill="currentColor" x="445" y="147" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">임포트 결과물 (변환된 에셋 데이터)</text>
  <!-- ArtifactDB -->
  <line x1="55" y1="166" x2="70" y2="166" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text fill="currentColor" x="75" y="171" font-size="10" font-family="monospace">ArtifactDB</text>
  <text fill="currentColor" x="445" y="171" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">임포트 결과 데이터베이스</text>
  <!-- SourceAssetDB -->
  <line x1="55" y1="190" x2="70" y2="190" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text fill="currentColor" x="75" y="195" font-size="10" font-family="monospace">SourceAssetDB</text>
  <text fill="currentColor" x="445" y="195" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.45">소스 에셋 정보 데이터베이스</text>

  <!-- Packages/ row -->
  <rect x="25" y="226" width="430" height="24" rx="3" fill="currentColor" fill-opacity="0.03"/>
  <text fill="currentColor" x="35" y="243" font-size="11" font-family="monospace" opacity="0.5">Packages/</text>

  <!-- ProjectSettings/ row -->
  <rect x="25" y="258" width="430" height="24" rx="3" fill="currentColor" fill-opacity="0.03"/>
  <text fill="currentColor" x="35" y="275" font-size="11" font-family="monospace" opacity="0.5">ProjectSettings/</text>
</svg>
</div>

<br>

그림처럼 `Library/` 안에는 변환된 에셋 데이터를 담는 `Artifacts/`와, 이를 관리하는 두 데이터베이스 `ArtifactDB`·`SourceAssetDB`가 들어 있습니다. 이 모두는 소스 에셋과 `.meta`만 있으면 다시 만들어지므로, Library 전체는 **언제든 재생성할 수 있습니다.**

실제로 이 폴더를 통째로 지워도, 에디터를 다시 열면 Unity가 `Assets`의 소스 에셋과 `.meta`를 읽어 임포트를 처음부터 다시 수행합니다. 다만 프로젝트가 크면 이 재임포트에 수 분에서 수십 분까지 걸리기도 합니다. 팀 작업이라면 **Unity Accelerator(캐시 서버)**로 이 부담을 줄일 수 있는데, 한 사람이 만들어 둔 임포트 결과를 다른 팀원이 네트워크로 받아 쓰기 때문입니다.

이렇게 언제든 다시 만들어지는 캐시이므로, Library 폴더는 **버전 관리에서 제외합니다.** `.gitignore`에 `Library/` 한 줄을 더해 두는 것이 표준 관행입니다.

한편 Library에는 같은 에셋이라도 **플랫폼마다 다른 변환 결과**가 저장됩니다. Android로 전환하면 텍스처가 **ASTC(Adaptive Scalable Texture Compression)**나 **ETC2(Ericsson Texture Compression 2)** 같은 GPU 압축 포맷으로 변환되고, iOS에서는 ASTC가 쓰입니다. 이처럼 플랫폼을 바꿀 때마다 캐시가 새로 갱신되므로, 플랫폼 전환(Switch Platform)에 시간이 걸릴 수 있습니다.

### Artifact 구조와 Asset Pipeline v2

Library는 이런 변환 결과물 하나하나를 **Artifact**라는 단위로 저장합니다. 같은 소스 에셋이라도 임포트 조건이 다르면 서로 다른 Artifact가 만들어지며, 방금 본 플랫폼 차이도 그 조건의 하나입니다.

Artifact를 결정하는 조건은 모두 네 가지입니다. 소스 에셋을 식별하는 GUID, Import Settings, Unity 버전, 플랫폼이며, 이 가운데 하나라도 바뀌면 기존 Artifact를 그대로 쓸 수 없어 새로 만듭니다.

<br>

<div style="text-align: center; margin: 1.5em 0;"><svg viewBox="0 0 480 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">Artifact 생성 조건</text>
  <!-- Input boxes -->
  <rect x="6" y="28" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="49" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">소스 에셋 (GUID)</text>
  <rect x="126" y="28" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="176" y="49" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">Import Settings</text>
  <rect x="246" y="28" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="296" y="49" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">플랫폼</text>
  <rect x="366" y="28" width="108" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="420" y="49" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">Unity 버전</text>
  <!-- Plus symbols between boxes -->
  <text x="116" y="50" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">+</text>
  <text x="236" y="50" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">+</text>
  <text x="356" y="50" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">+</text>
  <!-- Converging lines from each box down -->
  <line x1="56" y1="62" x2="220" y2="88" stroke="currentColor" stroke-width="1.2"/>
  <line x1="176" y1="62" x2="230" y2="88" stroke="currentColor" stroke-width="1.2"/>
  <line x1="296" y1="62" x2="250" y2="88" stroke="currentColor" stroke-width="1.2"/>
  <line x1="420" y1="62" x2="260" y2="88" stroke="currentColor" stroke-width="1.2"/>
  <!-- Arrow stem and head -->
  <line x1="240" y1="88" x2="240" y2="98" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,104 234,94 246,94" fill="currentColor"/>
  <!-- Output box -->
  <rect x="140" y="104" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="125" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Artifact (임포트 결과)</text>
  <!-- Note -->
  <text x="240" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.6">※ 위 조건 중 하나라도 바뀌면 Artifact 재생성</text>
</svg></div>

<br>

이 Artifact 시스템을 한층 다듬은 것이 Unity 2019.3부터 도입된 **Asset Pipeline v2**입니다. 바뀐 에셋만 다시 임포트하여 불필요한 재변환을 줄이고, 임포트 결과를 결정론적(deterministic)으로 만듭니다.

여기서 결정론적이라는 말은, 같은 소스 에셋을 같은 조건으로 임포트하면 어느 컴퓨터에서든 똑같은 결과물이 나온다는 뜻입니다. 따라서 팀원들이 각자의 로컬 `Library`에서 임포트해도 모두 같은 빌드 결과를 얻습니다.

---

## 텍스처 임포트

프로젝트의 여러 에셋 가운데 메모리와 빌드 용량을 가장 많이 차지하는 것은 대체로 텍스처입니다. 이미지 한 장의 용량은 작아 보여도, 캐릭터와 배경, UI에 쓰이는 텍스처가 모두 모이면 전체에서 차지하는 비중이 큽니다. 그만큼 Import Settings를 어떻게 설정하느냐에 따라 메모리와 용량을 아끼는 폭도 가장 큰 에셋입니다. 이 절에서는 임포트의 주요 옵션이 메모리 사용량과 빌드 크기를 어떻게 바꾸는지 하나씩 살펴봅니다.

### 소스 포맷에서 엔진 포맷으로

텍스처를 프로젝트에 넣어도 그 PNG나 PSD 파일이 그대로 게임에 들어가지는 않습니다. Unity는 임포트 과정에서 이 파일을 빌드 대상 플랫폼이 GPU에서 바로 읽을 수 있는 압축 포맷으로 변환합니다. 같은 텍스처라도 Android에서는 ASTC 6x6, iOS에서는 ASTC 4x4, PC에서는 BC7처럼, 어느 플랫폼으로 빌드하느냐에 따라 서로 다른 포맷으로 들어갑니다.

<br>

<div style="text-align: center;">
<svg viewBox="0 0 580 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="290" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">텍스처 임포트 과정</text>
  <!-- Left box: 소스 파일 -->
  <rect x="10" y="30" width="140" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="80" y="50" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">소스 파일</text>
  <line x1="22" y1="57" x2="138" y2="57" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="28" y="76" font-size="11" font-family="sans-serif">PNG (24bit)</text>
  <text fill="currentColor" x="28" y="96" font-size="11" font-family="sans-serif">PSD (32bit)</text>
  <text fill="currentColor" x="28" y="116" font-size="11" font-family="sans-serif">TGA (32bit)</text>
  <text fill="currentColor" x="28" y="136" font-size="11" font-family="sans-serif">EXR (HDR)</text>
  <!-- Center: Import funnel -->
  <line x1="150" y1="76" x2="218" y2="95" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="150" y1="96" x2="218" y2="95" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="150" y1="116" x2="218" y2="95" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="150" y1="136" x2="218" y2="95" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <rect x="220" y="72" width="100" height="46" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="270" y="100" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Import</text>
  <line x1="320" y1="95" x2="360" y2="76" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="320" y1="95" x2="360" y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="320" y1="95" x2="360" y2="116" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="320" y1="95" x2="360" y2="136" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <!-- Right box: 플랫폼별 결과 -->
  <rect x="362" y="30" width="208" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="466" y="50" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">플랫폼별 결과</text>
  <line x1="374" y1="57" x2="558" y2="57" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="378" y="76" font-size="11" font-family="sans-serif">Android: ASTC 6x6</text>
  <text fill="currentColor" x="378" y="96" font-size="11" font-family="sans-serif">iOS: ASTC 4x4</text>
  <text fill="currentColor" x="378" y="116" font-size="11" font-family="sans-serif">PC: BC7</text>
  <text fill="currentColor" x="378" y="136" font-size="11" font-family="sans-serif">Console: 플랫폼별 포맷</text>
  <!-- Bottom box: Import Settings -->
  <rect x="140" y="180" width="300" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="290" y="200" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">Import Settings에 따라 결정</text>
  <line x1="155" y1="207" x2="425" y2="207" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="160" y="224" font-size="10" font-family="sans-serif">Max Size · 압축 포맷 · Mipmap 생성 여부</text>
  <text fill="currentColor" x="160" y="242" font-size="10" font-family="sans-serif">sRGB / Linear · Read/Write Enabled</text>
  <!-- Arrow from settings to import box -->
  <line x1="270" y1="178" x2="270" y2="122" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <polygon points="270,118 266,126 274,126" fill="currentColor"/>
</svg>
</div>

<br>

여기서 결과물을 결정하는 것은 소스 파일이 PNG냐 PSD냐 하는 포맷이 아니라 Import Settings입니다. Unity가 소스 파일에서 가져오는 것은 픽셀 데이터뿐이고, 이 픽셀을 Import Settings에 맞춰 변환하기 때문입니다. 이 과정에서 PSD의 레이어 구조처럼 픽셀이 아닌 정보는 결과물에 포함되지 않습니다. 따라서 소스 포맷 자체는 결과물에 영향을 주지 않으므로, 아티스트가 작업하기 편한 포맷을 선택하면 됩니다. 정작 메모리와 품질을 바꾸는 것은 그다음에 지정하는 Import Settings 항목들입니다.

### 텍스처 유형 설정

그 Import Settings 가운데 가장 먼저 정하는 항목이 **Texture Type**입니다. 이 텍스처를 어디에 쓸 것인지, 그 용도를 정하는 설정입니다. 용도에 따라 Unity가 텍스처를 다루는 방식이 달라지기 때문에, 색을 보정할지, 어떤 포맷으로 압축할지, 어떤 기능을 열어 줄지가 모두 이 선택에서 결정됩니다. 그래서 다른 설정에 앞서 유형부터 정해야 합니다.

가장 기본이 되는 것은 화면에 보일 색을 담은 텍스처입니다. 캐릭터의 피부나 벽의 무늬처럼 눈에 보이는 표면 색이 여기에 들어가며, 이런 텍스처에는 **Default**를 씁니다. Albedo와 Diffuse, 스스로 빛나는 부분을 나타내는 Emission 맵이 모두 여기에 해당합니다. Default로 임포트하면 Unity는 이 픽셀을 색으로 다루어, 화면에 제대로 보이도록 sRGB 감마 보정을 기본으로 적용합니다.

표면의 디테일을 셰이더 계산에 넘기는 텍스처는 다루는 방식이 다릅니다. 대표적인 것이 노멀맵으로, 픽셀에는 색이 아니라 그 지점에서 표면이 어느 쪽을 향하는지 가리키는 방향 벡터가 들어 있습니다. 이런 텍스처에는 **Normal Map**을 지정하는데, 그러면 Unity는 값을 방향으로 해석해 색 보정을 끄고 방향 데이터에 맞춘 전용 포맷으로 압축합니다. 만약 노멀맵을 Default로 둔 채 임포트하면, Unity가 방향 값을 색으로 여겨 sRGB 보정을 적용합니다. 색에 맞춘 보정은 방향 값을 왜곡하므로, 표면이 가리키는 방향이 틀어지고 그 노멀맵으로 계산한 조명까지 어긋납니다.

같은 계산용 데이터라도 거칠기나 금속성처럼 픽셀마다 값 하나면 충분한 경우가 있습니다. 표면의 일부를 가리는 마스크나 높이를 담은 하이트맵도 그렇습니다. 이런 텍스처는 **Single Channel**로 지정해 R이나 Alpha 한 채널만 저장하면, 나머지 채널을 만들지 않아 메모리를 아낍니다. 이 역시 Default로 두면 쓰지도 않는 채널까지 저장되어 메모리를 더 차지합니다.

지금까지가 3D 표면에 입히는 텍스처였다면, 화면에 직접 그리는 2D 이미지는 쓰임의 영역이 다릅니다. UI 아이콘이나 버튼, 2D 게임의 캐릭터와 배경에는 **Sprite (2D/UI)**를 씁니다. 이 유형이라야 Sprite Editor에서 이미지를 여러 조각으로 잘라 쓰거나 그 조각들을 하나의 아틀라스로 묶을 수 있습니다. 모두 Sprite로 지정한 이미지에서만 동작하는 기능입니다.

주요 유형은 이 네 가지이고, 그 밖에 마우스 커서에 쓰는 Cursor, 라이트 쿠키에 쓰는 Cookie, HDR로 인코딩된 라이트맵 전용인 Lightmap처럼 특수한 용도를 위한 유형도 있습니다.

정리하면, Texture Type은 텍스처의 용도를 Unity에 알려 주는 첫 설정이고, 이 선택에서 색 보정과 압축 방식, 쓸 수 있는 기능이 함께 결정됩니다. 용도에 맞게 지정하면 Unity가 알맞게 처리하지만, 어긋나게 두면 화면이 틀어지거나 메모리를 헛되이 씁니다. 그러므로 텍스처를 임포트할 때는 그 쓰임부터 정확히 정하는 것이 먼저입니다.

### sRGB vs Linear

색을 8비트로 저장할 때는 256단계를 실제 밝기에 똑같은 간격으로 나누어 담지 않습니다. 사람의 눈이 밝기를 고르게 느끼지 않기 때문입니다. 눈은 어두운 영역의 차이에는 민감하지만 밝은 영역의 차이에는 둔감해서, 단계를 균등하게 나누면 정작 민감한 어두운 영역에서 단계가 모자라 색이 띠처럼 끊겨 보이는 밴딩(banding)이 생깁니다. 그래서 어두운 쪽에 더 많은 단계를 몰아 주는 비선형 변환을 거쳐 색을 저장하는데, 이 변환이 **감마 인코딩**이고 그 결과를 담는 색 공간이 **sRGB**입니다. 우리가 다루는 색상 이미지는 대부분 이 sRGB로 저장됩니다.

문제는 이렇게 저장한 색을 셰이더가 그대로 쓸 수 없다는 데 있습니다. 셰이더의 조명 계산은 빛의 물리를 따르는데, 현실에서 빛은 두 광원이 겹치면 그 세기가 그대로 더해집니다. 이렇게 선형(Linear)으로 합쳐지는 빛과 달리 sRGB로 저장된 색은 감마 인코딩을 거친 비선형 값이어서, 그대로 조명 계산에 넣으면 밝기가 틀어집니다. 이 문제를 바로잡는 설정이 sRGB 옵션입니다.

sRGB 옵션을 켜면, GPU는 텍스처를 샘플링하는 시점에 감마 인코딩을 풀어 선형 값으로 되돌린 뒤 셰이더에 넘깁니다. 저장은 밴딩을 막는 sRGB 형태로 해 두고, 계산할 때만 선형으로 바꿔 씁니다. 그래서 색을 담은 Default 유형에서는 이 옵션이 기본으로 켜져 있습니다.

반대로 색이 아닌 텍스처에서는 이 옵션이 꺼져 있어야 합니다. 노멀맵의 방향 벡터나 마스크의 가림 값, 하이트맵의 높이는 처음부터 감마 인코딩과 무관한 그대로의 수치입니다. 여기에 sRGB를 켜 두면 GPU가 이 수치를 인코딩된 색으로 잘못 해석해 디코딩하므로, 원래 값이 변형되고 그 텍스처를 쓰는 계산까지 어긋납니다. 그래서 Normal Map이나 Single Channel 유형에서는 sRGB가 기본으로 꺼져 있습니다.

결국 sRGB 옵션은, 색은 선형으로 되돌려 정확히 계산되게 하고 수치는 원래 값 그대로 두게 하는 설정입니다.

### Max Size: 메모리와 품질의 핵심 설정

Texture Type과 sRGB가 텍스처의 픽셀을 어떻게 해석할지 정하는 설정이라면, 지금부터 볼 설정들은 그 텍스처가 메모리를 얼마나 차지하는지를 좌우합니다. 그중에서도 영향이 가장 큰 항목이 **Max Size**입니다. 텍스처의 해상도를 낮춰 메모리를 크게 줄이기 때문입니다.

Max Size는 임포트를 마친 텍스처가 가질 수 있는 가로·세로 해상도의 상한입니다. 소스 파일이 4096x4096이더라도 Max Size를 1024로 정하면, 이미지의 일부만 잘라 쓰는 것이 아니라 전체가 1024x1024로 축소되어 들어옵니다.

<br>

**Max Size에 따른 메모리 변화** (ASTC 6x6 기준, 밉맵 포함, 소스: 4096 x 4096)

| Max Size | 해상도 | 메모리 (약) |
|---|---|---|
| 4096 | 4096 x 4096 | 9.5 MB |
| 2048 | 2048 x 2048 | 2.37 MB |
| 1024 | 1024 x 1024 | 0.59 MB |
| 512 | 512 x 512 | 0.15 MB |
| 256 | 256 x 256 | 0.04 MB |

표를 보면 Max Size를 한 단계 내릴 때마다 메모리가 약 1/4로 줄어듭니다. 한 단계를 낮추면 가로와 세로가 각각 절반이 되어, 넓이로 따진 전체 픽셀 수가 1/4로 줄기 때문입니다. 텍스처가 차지하는 메모리는 픽셀 수에 비례하므로, 픽셀 수가 1/4이 되면 메모리도 그만큼 내려갑니다.

다만 해상도를 낮추면 그만큼 텍스처가 화면에서 흐릿해지므로, 모든 텍스처를 일률적으로 낮출 수는 없습니다. 어디까지 낮출지는 그 텍스처가 화면에서 차지하는 비중에 맞춰 정해야 합니다. 예를 들어 가까이에서 크게 보이는 주인공 캐릭터는 2048로 두고, 멀리 있는 배경 오브젝트는 512로, 작은 UI 아이콘은 256으로 낮춥니다. 이렇게 눈에 잘 띄지 않는 텍스처부터 해상도를 내리면 체감 화질은 거의 해치지 않으면서 전체 텍스처 메모리를 크게 줄일 수 있어, 메모리가 빠듯한 모바일에서 특히 효과가 큽니다.

### Read/Write Enabled의 비용

Max Size가 텍스처 한 장의 크기를 줄이는 설정이라면, **Read/Write Enabled**는 텍스처의 픽셀을 CPU에서 직접 읽고 수정하도록 허용하는 옵션입니다. `Texture2D.GetPixel()`로 특정 픽셀의 색을 읽거나 `Texture2D.SetPixel()`로 값을 바꾸는 코드는 이 옵션이 켜져 있어야 동작합니다. 그런데 이 옵션을 켜면 텍스처가 메모리를 두 배로 차지합니다.

<br>

<div><svg viewBox="0 0 480 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">Read/Write Enabled의 메모리 영향</text>
  <!-- Left: OFF -->
  <text x="110" y="44" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Read/Write 꺼짐</text>
  <rect x="20" y="56" width="180" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="83" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">GPU 메모리에만 존재</text>
  <text x="110" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">텍스처 1장 분량</text>
  <text x="110" y="148" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">1×</text>
  <!-- Right: ON -->
  <text x="370" y="44" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Read/Write 켜짐</text>
  <rect x="280" y="56" width="180" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="370" y="83" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">GPU 메모리 (렌더링)</text>
  <rect x="280" y="100" width="180" height="44" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="370" y="127" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">CPU 메모리 (사본)</text>
  <text x="370" y="164" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">2×</text>
  <!-- Annotation -->
  <text x="240" y="174" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">메모리 사용량이 2배</text>
</svg></div>

<br>

이렇게 메모리가 두 배가 되는 것은, 렌더링용으로 GPU에 올라간 텍스처와 별개로 CPU 코드가 언제든 픽셀에 접근할 수 있도록 Unity가 CPU 메모리에도 같은 데이터의 사본을 따로 유지하기 때문입니다. 그래서 2048x2048 RGBA32 텍스처라면 GPU에 16MB, CPU 사본에 다시 16MB, 합쳐서 32MB를 차지합니다. 따라서 CPU에서 픽셀을 읽거나 수정할 일이 없는 텍스처는 이 옵션을 꺼 두어야 합니다.

### Mipmap 생성

3D 오브젝트는 카메라와의 거리에 따라 화면에서 차지하는 크기가 계속 바뀝니다. 가까이 있을 때는 고해상도 텍스처가 필요하지만, 멀리 있으면 같은 표면도 몇 픽셀로만 그려질 수 있습니다. 원본 텍스처 하나만 있으면 작은 영역을 그릴 때도 고해상도 원본을 샘플링해야 하므로 대역폭을 낭비하고, 촘촘한 무늬가 몇 픽셀 안에 눌리면서 샘플링 결과도 불안정해집니다.

**Generate Mip Maps**를 켜면 Unity는 원본 텍스처를 절반 크기로 줄이고, 그 결과를 다시 절반으로 줄이는 방식으로 여러 단계의 축소본을 만듭니다. 이렇게 단계별로 준비된 축소본을 **밉맵(Mipmap)**이라고 하며, 각 축소본은 하나의 **밉 레벨**입니다. 전체 밉맵 체인은 `1 + 1/4 + 1/16 + ...`처럼 더해지므로, 원본만 둘 때보다 텍스처 메모리가 약 33% 늘어납니다.

<br>

<div><svg viewBox="0 0 460 175" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">밉맵 체인</text>
  <!-- All boxes bottom-aligned at y=120 -->
  <!-- Level 0: 96×96 -->
  <rect x="20" y="24" width="96" height="96" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="68" y="76" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1024×1024</text>
  <text x="68" y="136" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">Level 0 (원본)</text>
  <!-- Arrow 0→1 -->
  <line x1="118" y1="96" x2="138" y2="96" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- Level 1: 48×48 -->
  <rect x="140" y="72" width="48" height="48" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="164" y="100" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">512×512</text>
  <text x="164" y="136" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">Level 1</text>
  <!-- Arrow 1→2 -->
  <line x1="190" y1="108" x2="210" y2="108" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- Level 2: 24×24 -->
  <rect x="212" y="96" width="24" height="24" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="224" y="136" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">Level 2</text>
  <!-- Arrow 2→3 -->
  <line x1="238" y1="114" x2="258" y2="114" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- Level 3: 12×12 -->
  <rect x="260" y="108" width="12" height="12" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- Arrow 3→4 -->
  <line x1="274" y1="117" x2="294" y2="117" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- Level 4: 6×6 -->
  <rect x="296" y="114" width="6" height="6" rx="1" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- Dots -->
  <text x="320" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">…</text>
  <!-- Level N: 3×3 -->
  <rect x="344" y="117" width="3" height="3" rx="0.5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text x="345" y="136" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">Level N</text>
  <!-- Annotation -->
  <text x="230" y="155" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">밉맵을 포함하면 메모리가 약 33% 증가</text>
  <text x="230" y="168" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">(1 + 1/4 + 1/16 + 1/64 + … ≈ 1.33배)</text>
</svg></div>

<br>

밉맵의 첫 번째 효과는 메모리 대역폭 절감입니다. 예를 들어 어떤 표면이 화면에서 4×4 픽셀 정도로만 보인다면, 1024×1024 원본 전체를 기준으로 샘플링할 필요가 없습니다. GPU가 화면 크기에 가까운 낮은 밉 레벨을 선택하면 읽어야 할 텍셀 수가 적어지고, 텍스처 샘플링에 필요한 메모리 대역폭도 작아집니다.

두 번째 효과는 텍스처 앨리어싱 감소입니다. 체크무늬나 얇은 격자처럼 변화가 빠른 무늬를 멀리서 작게 그리면, 여러 텍셀이 하나의 화면 픽셀에 섞여 들어갑니다. 그러면 카메라가 조금만 움직여도 GPU가 읽는 텍셀 조합이 달라지고, 그 차이가 무늬의 깜빡임이나 흔들림으로 보입니다. 밉맵은 미리 다운샘플링된 축소본을 사용하므로, 멀리서 구분되지 않을 고주파 성분을 줄인 상태로 텍스처를 읽게 해 줍니다. 그래서 원본만 읽을 때보다 무늬의 흔들림과 깜빡임이 줄어듭니다.

UI 텍스처는 보통 반대입니다. 일반적인 Screen Space UI의 버튼과 아이콘은 카메라에서 멀어지는 3D 표면이 아니라, 정해진 화면 크기에서 또렷하게 보여야 하는 요소입니다. 이런 텍스처에 밉맵을 켜면 추가 축소본 때문에 메모리가 늘고, 상황에 따라 가장자리나 아틀라스 경계가 흐려질 수 있습니다. 그래서 일반적인 UI 텍스처는 **Generate Mip Maps**를 끕니다.

정리하면, 거리에 따라 화면 크기가 바뀌는 3D 텍스처에는 밉맵을 켜는 것이 기본입니다. 메모리 증가가 부담된다면 밉맵 자체를 끄기보다 **Texture Streaming**(Mipmap Streaming)으로 관리합니다. Texture Streaming은 카메라에 필요한 밉 레벨만 메모리에 유지하는 기능입니다. Quality Settings에서 **Texture Streaming**을 켜고, 텍스처 Import Settings에서 **Streaming Mipmaps**를 활성화한 뒤 메모리 예산(Memory Budget)을 지정하면 Unity가 그 범위 안에서 밉 레벨을 조정합니다.

---

## 모델 임포트

텍스처가 표면의 색과 질감을 담는다면, 모델은 그 표면이 놓일 형태를 담습니다. 캐릭터의 실루엣, 배경 오브젝트의 윤곽, 애니메이션이 움직일 뼈대는 모두 모델 데이터에서 시작됩니다.

FBX나 OBJ 파일도 Unity가 런타임에서 그대로 쓰는 데이터는 아닙니다. Unity는 파일 안의 정점, 인덱스, 노멀, UV, 본 정보를 읽어 엔진 내부의 메쉬 데이터로 변환합니다. 이때 제작 도구마다 다른 좌표축과 단위를 Unity 기준으로 맞추고, Import Settings에 따라 압축과 최적화도 적용합니다.

### 좌표축 변환과 Scale Factor

같은 모델이라도 어느 도구에서 만들었느냐에 따라 좌표축과 단위 관례가 제각각입니다. Maya는 오른손 좌표계에 Y축이 위를 향하고 센티미터를 단위로 쓰고, Blender는 같은 오른손 좌표계라도 Z축이 위를 향하며 단위는 미터입니다. 3ds Max 역시 오른손 Z-up이지만 인치나 센티미터를 단위로 씁니다.

반면 Unity는 왼손 좌표계에 Y축이 위를 향하고 미터를 기준으로 삼습니다. 따라서 외부 모델을 들여올 때는 좌표축과 단위를 모두 Unity 기준에 맞추는 변환이 필요합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;"><svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">좌표계 차이</text>
  <!-- Maya (Left) -->
  <text x="120" y="42" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Maya (오른손, Y-up)</text>
  <!-- Maya axes origin at (120, 130) -->
  <!-- Y axis (up) -->
  <line x1="120" y1="130" x2="120" y2="62" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="120,58 116,66 124,66" fill="currentColor"/>
  <text x="130" y="62" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Y</text>
  <!-- X axis (right) -->
  <line x1="120" y1="130" x2="196" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="200,130 192,126 192,134" fill="currentColor"/>
  <text x="206" y="134" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">X</text>
  <!-- Z axis (diagonal toward viewer) -->
  <line x1="120" y1="130" x2="76" y2="162" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="73,165 82,163 79,155" fill="currentColor"/>
  <text x="58" y="174" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Z</text>
  <text x="106" y="186" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">(화면 밖으로)</text>
  <!-- Unity (Right) -->
  <text x="390" y="42" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Unity (왼손, Y-up)</text>
  <!-- Unity axes origin at (390, 130) -->
  <!-- Y axis (up) -->
  <line x1="390" y1="130" x2="390" y2="62" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="390,58 386,66 394,66" fill="currentColor"/>
  <text x="400" y="62" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Y</text>
  <!-- X axis (right) -->
  <line x1="390" y1="130" x2="466" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="470,130 462,126 462,134" fill="currentColor"/>
  <text x="476" y="134" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">X</text>
  <!-- Z axis (diagonal into screen - lower right, mirrored from Maya) -->
  <line x1="390" y1="130" x2="434" y2="162" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="437,165 428,163 431,155" fill="currentColor"/>
  <text x="452" y="174" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Z</text>
  <text x="420" y="186" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">(화면 안으로)</text>
  <!-- Annotations -->
  <text x="260" y="206" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">임포트 시 좌표축 변환 자동 수행 · Scale Factor로 단위 변환 (FBX의 기본값: 0.01)</text>
</svg></div>

<br>

이 가운데 좌표축 변환은 임포트 시점에 Unity가 자동으로 처리합니다. 개발자가 값을 지정하지 않아도 모델이 Unity의 축 방향에 맞게 정렬되어 들어옵니다.

단위 변환은 **Scale Factor**가 맡습니다. 임포트할 때 모델의 모든 좌표에 이 값을 곱해, 소스 파일의 단위를 Unity의 미터로 환산합니다. 
만약, Scale Factor가 잘못 지정되면 모델이 의도한 크기보다 크거나 작게 임포트됩니다.

### Mesh Compression

**Mesh Compression**은 메쉬 데이터를 빌드 파일에 담을 때 얼마나 강하게 압축할지를 정하는 옵션입니다. Off, Low, Medium, High 네 단계가 있고, 단계를 높일수록 용량이 더 줄어듭니다.

다만 압축 단계를 높이면 정점 좌표를 더 적은 비트로 저장하게 됩니다. 이때 0.123456처럼 연속적인 좌표 값은 0.12 같은 정해진 간격의 값으로 근사되는데, 이 처리를 **양자화(quantization)**라고 합니다. 압축이 강할수록 값 사이의 간격이 넓어지고, 그만큼 정점이 원래 위치에서 벗어납니다. 그 결과 크기가 작거나 형태가 정교한 모델에서는 표면이 거칠어지거나 가장자리가 틀어지는 아티팩트가 나타날 수 있으므로, 압축 단계를 높인 뒤에는 모델의 형태를 직접 확인하는 것이 좋습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;"><svg viewBox="0 0 500 140" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <text x="250" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">Mesh Compression의 영향 범위</text>
  <!-- Left box: 줄이는 것 (solid stroke) -->
  <rect x="10" y="30" width="230" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="125" y="52" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">줄이는 것</text>
  <line x1="30" y1="59" x2="220" y2="59" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text x="125" y="82" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">디스크(빌드 파일)에서의 크기</text>
  <text x="125" y="120" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.5">빌드 용량 절감</text>
  <!-- Right box: 줄이지 않는 것 (dashed stroke) -->
  <rect x="260" y="30" width="230" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="375" y="52" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">줄이지 않는 것</text>
  <line x1="280" y1="59" x2="470" y2="59" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text x="375" y="82" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">런타임 메모리 사용량</text>
  <text x="375" y="104" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">로드 시 압축 해제하여</text>
  <text x="375" y="120" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">원본 크기로 메모리에 배치</text>
</svg></div>

<br>

이때, 압축 단계를 높여도 런타임 메모리 사용량은 줄지 않습니다. 메쉬는 로드될 때 압축이 풀려 원래 크기로 메모리에 올라가므로, 이 옵션으로 아낄 수 있는 것은 빌드 파일의 크기뿐입니다.

### Read/Write Enabled (메쉬)

텍스처에서 살펴본 **Read/Write Enabled**는 메쉬에도 있습니다. 메쉬 데이터는 로드된 뒤 GPU로 올라가고, 기본 설정에서는 CPU 쪽 사본이 곧바로 해제됩니다. 이 옵션을 켜면 그 사본이 CPU 메모리에 그대로 남아, 같은 메쉬가 GPU와 CPU 양쪽에 존재하면서 메모리를 두 배로 차지합니다.

따라서 이 옵션은 런타임에 메쉬 데이터를 직접 읽거나 바꿔야 할 때만 켭니다. 지형을 절차적으로 생성하거나 정점을 움직여 메쉬 형태를 바꾸는 경우, 또는 `Mesh.vertices`로 정점 데이터를 읽어 오는 경우가 여기에 해당합니다. 반면 배경이나 건물, 소품처럼 한 번 배치한 뒤 형태가 바뀌지 않는 정적 메쉬는 CPU 사본이 필요 없으므로, 이 옵션을 꺼 두는 것이 좋습니다.

### Optimize Mesh

**Optimize Mesh**는 정점(Vertex)과 인덱스(Index)의 배열 순서를 조정해, GPU가 같은 정점을 여러 번 변환하는 낭비를 줄이는 옵션입니다.

메쉬는 정점을 모아 둔 정점 버퍼(Vertex Buffer)와, 각 삼각형이 그중 어떤 정점을 사용하는지 가리키는 인덱스 버퍼(Index Buffer)로 이루어집니다. 인접한 삼각형은 모서리를 맞대며 같은 정점을 공유하므로, 정점 하나가 여러 삼각형의 인덱스에 걸쳐 참조됩니다. GPU는 이 정점들을 정점 셰이더에서 하나씩 변환하는데, 같은 정점이 참조될 때마다 그 변환을 처음부터 반복한다면 그만큼 계산이 중복됩니다.

이 중복을 줄이기 위해 GPU는 한 번 변환된 정점을 곧바로 버리지 않고 **post-transform cache**라는 작은 내부 캐시에 담아 둡니다. 곧이어 다른 삼각형이 같은 정점을 참조하면, 캐시에 남은 결과를 그대로 사용하므로 재계산이 필요 없습니다.

다만 이 캐시는 크기가 작아서, 함께 사용되는 정점들이 인덱스 순서에서 멀리 떨어져 있으면 다시 참조되기 전에 캐시에서 밀려납니다. 밀려난 정점은 다음에 참조될 때 다시 변환되므로, 정점을 어떤 순서로 배열하느냐에 따라 전체 변환 횟수가 달라집니다.

Optimize Mesh를 켜면 Unity가 임포트 시점에 함께 사용되는 정점들을 인덱스 순서에서 가까이 모아 재배열합니다. 그 결과 캐시에 남아 있는 동안 정점이 다시 참조될 가능성이 높아져, 캐시 히트율이 오르고 정점 셰이더의 중복 변환이 줄어듭니다. 재배열은 임포트할 때 한 번만 이루어지므로, 런타임에는 추가 비용이 붙지 않습니다.

주의할 점은 정점 번호에 의존하는 코드입니다. Optimize Mesh는 원본 모델의 정점 순서를 보존하지 않으므로, 임포트된 메쉬에서 `Mesh.vertices[i]`가 원본의 i번째 정점을 가리킨다는 보장이 없어집니다. 이 때문에 Read/Write Enabled를 켜고 특정 인덱스의 정점을 직접 읽거나 수정하는 코드가 있다면, 최적화 뒤에는 의도와 다른 정점을 다룰 수 있습니다. 반대로 런타임 코드가 정점 인덱스에 직접 의존하지 않는다면 화면에 그려지는 결과는 그대로입니다. 이 경우에는 정점 셰이더의 중복 변환을 줄일 수 있으므로 Optimize Mesh를 켜 두는 편이 좋습니다.

### Animation 임포트

FBX에는 메쉬와 함께 뼈대와 애니메이션 데이터가 들어 있는 경우가 있습니다. 이 데이터에 관한 설정은 Import Settings의 **Rig** 탭과 **Animation** 탭에 모여 있습니다. 앞의 옵션들이 모델의 형태와 비용을 다뤘다면, 이 두 탭은 그 모델을 어떤 방식으로 움직일지를 결정합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;"><svg viewBox="0 0 480 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">Animation 임포트 설정</text>
  <!-- Rig 탭 -->
  <text x="20" y="42" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Rig 탭</text>
  <rect x="16" y="50" width="448" height="120" rx="6" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="32" y="72" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Animation Type</text>
  <!-- None -->
  <text x="44" y="96" font-size="10" font-weight="bold" font-family="monospace" fill="currentColor">None</text>
  <text x="130" y="96" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">애니메이션 사용 안 함</text>
  <!-- Legacy -->
  <text x="44" y="114" font-size="10" font-weight="bold" font-family="monospace" fill="currentColor">Legacy</text>
  <text x="130" y="114" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">구버전 시스템 (비권장)</text>
  <!-- Generic -->
  <text x="44" y="132" font-size="10" font-weight="bold" font-family="monospace" fill="currentColor">Generic</text>
  <text x="130" y="132" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">범용, 프롭·동물·메카닉 등에 적합</text>
  <!-- Humanoid -->
  <text x="44" y="150" font-size="10" font-weight="bold" font-family="monospace" fill="currentColor">Humanoid</text>
  <text x="130" y="150" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">인간형 리깅, 리타겟팅 가능</text>
  <rect x="38" y="140" width="420" height="16" rx="3" fill="currentColor" fill-opacity="0.06" stroke="none"/>
  <!-- Animation 탭 -->
  <text x="20" y="196" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Animation 탭</text>
  <rect x="16" y="204" width="448" height="96" rx="6" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="32" y="226" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Clip 분리</text>
  <text x="32" y="248" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">하나의 FBX에 포함된 연속 애니메이션을</text>
  <text x="32" y="264" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">시작/종료 프레임으로 잘라서 개별 Clip으로 분리</text>
  <text x="32" y="288" font-size="10" font-family="monospace" fill="currentColor" opacity="0.5">예: Idle (0~30)  Walk (31~60)  Run (61~90)</text>
</svg></div>

<br>

Rig 탭의 **Animation Type**에는 네 가지 선택지가 있지만, 애니메이션을 쓰지 않는 None과 구버전 시스템인 Legacy를 제외하면 실제 선택은 **Generic**과 **Humanoid**로 좁혀집니다. 두 타입의 차이는 애니메이션을 어느 뼈대를 기준으로 적용하느냐에 있습니다.

**Generic**은 모델 자체의 뼈대를 그대로 사용해 애니메이션을 재생하는 타입으로, 문이나 차량, 소품, 동물, 기계처럼 인간형이 아닌 대상에 적합합니다. 다만 애니메이션이 그 뼈대 구조에 종속되므로, 뼈대가 다른 모델에는 같은 애니메이션을 재사용할 수 없습니다.

**Humanoid**는 인간형 캐릭터에 한해 이 제약을 해소합니다. Humanoid로 임포트하면 Unity는 모델의 뼈대를 미리 정의된 표준 인간형 골격에 대응시키는 매핑 정보인 **Avatar**를 만들어 둡니다. 애니메이션이 이 표준 골격을 기준으로 적용되므로, 매핑을 갖춘 인간형 캐릭터 사이에서는 뼈대가 서로 달라도 같은 애니메이션을 재사용할 수 있습니다. 이 재사용 방식을 **리타겟팅(Retargeting)**이라고 하며, 주인공의 걷기 애니메이션을 체형이 다른 NPC에 그대로 적용하는 경우가 여기에 해당합니다.

그 대신 Humanoid는 런타임에 표준 골격의 포즈를 각 캐릭터의 실제 뼈대 구조로 변환해야 하므로, 자체 뼈대를 그대로 사용하는 Generic보다 CPU 비용이 더 듭니다. 따라서 리타겟팅이 필요한 캐릭터에만 Humanoid를 사용하고, 인간형 캐릭터라도 애니메이션을 공유하지 않는다면 Generic을 선택해 변환 비용을 줄이는 것이 좋습니다.

제작 도구에서는 여러 동작을 한 타임라인에 이어 붙여 하나의 FBX로 내보내기도 합니다. 이런 파일에는 동작들이 연속된 프레임 구간으로 담겨 있어, 이 상태로는 각 동작을 따로 재생할 수 없습니다. **Animation** 탭에서는 Animation Type이 Generic이든 Humanoid든, 동작마다 시작 프레임과 종료 프레임을 지정해 Idle(0~30), Walk(31~60), Run(61~90) 같은 개별 Clip으로 분리할 수 있습니다.

---

## 오디오 임포트

같은 사운드 파일이라도 임포트 설정에 따라 메모리 사용량과 재생할 때의 CPU 디코딩 비용이 달라집니다. 다만 두 비용을 함께 줄이기는 어렵습니다. 사운드를 압축된 채로 두면 메모리를 아끼는 대신 재생할 때마다 디코딩을 거쳐야 하고, 미리 풀어 두면 재생은 가벼워지지만 압축을 푼 크기만큼 메모리를 차지하기 때문입니다.

균형을 어디에 둘지는 사운드마다 다릅니다. 짧고 자주 재생되는 효과음은 즉시 재생이 우선이고, 몇 분씩 이어지는 BGM은 메모리 절약이 우선입니다. 이 차이에 맞춰 정하는 설정이 압축 방식인 코덱과 로드 방식인 Load Type입니다.

### 소스 포맷과 코덱 변환

오디오에도 소스 에셋과 임포트 에셋의 구분이 그대로 적용됩니다. 프로젝트에 넣은 WAV, MP3, OGG 파일은 소스 에셋으로 남고, 게임에서 실제로 재생되는 것은 임포트 과정에서 Import Settings에 지정한 코덱으로 변환된 데이터입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;"><svg viewBox="0 0 540 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">오디오 임포트 과정</text>
  <!-- Left: Source boxes -->
  <rect x="10" y="36" width="100" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="56" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">WAV (PCM)</text>
  <rect x="10" y="76" width="100" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="96" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">MP3</text>
  <rect x="10" y="116" width="100" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">OGG</text>
  <!-- Converging lines to Import box -->
  <line x1="110" y1="51" x2="190" y2="86" stroke="currentColor" stroke-width="1.2"/>
  <line x1="110" y1="91" x2="190" y2="91" stroke="currentColor" stroke-width="1.2"/>
  <line x1="110" y1="131" x2="190" y2="96" stroke="currentColor" stroke-width="1.2"/>
  <!-- Center: Import box -->
  <rect x="192" y="68" width="96" height="46" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="96" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif" fill="currentColor">Import</text>
  <!-- Fanning lines to output boxes -->
  <line x1="288" y1="80" x2="350" y2="51" stroke="currentColor" stroke-width="1.2"/>
  <line x1="288" y1="91" x2="350" y2="91" stroke="currentColor" stroke-width="1.2"/>
  <line x1="288" y1="102" x2="350" y2="131" stroke="currentColor" stroke-width="1.2"/>
  <!-- Right: Output codec boxes -->
  <rect x="352" y="30" width="180" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="442" y="46" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">Vorbis</text>
  <text x="442" y="60" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">손실 압축, 품질 조절 가능</text>
  <rect x="352" y="74" width="180" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="442" y="90" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">ADPCM</text>
  <text x="442" y="104" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">중간 압축, 빠른 디코딩</text>
  <rect x="352" y="118" width="180" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="442" y="134" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="currentColor">PCM</text>
  <text x="442" y="148" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.5">무압축, 최고 품질</text>
  <!-- Note -->
  <text x="270" y="186" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor" opacity="0.6">※ 소스 포맷과 무관하게, 임포트 후 코덱은 Import Settings로 결정</text>
</svg></div>

<br>

임포트 후 코덱은 Vorbis, ADPCM, PCM 세 가지 가운데 지정합니다. **Vorbis**는 품질을 조절할 수 있는 손실 압축 코덱으로, 용량 대비 음질이 좋아 BGM이나 길게 이어지는 효과음처럼 데이터량이 많은 소리에 주로 사용합니다.

반면 자주 재생되는 짧은 효과음은 용량보다 재생할 때마다 드는 디코딩 비용이 더 중요합니다. **ADPCM**(Adaptive Differential PCM)은 16비트 샘플을 4비트로 압축하는 단순한 방식이라 디코딩이 빠르고, 용량도 원본 대비 3.5~4배 정도 줄어들어 이런 소리에 잘 맞습니다. **PCM**(Pulse Code Modulation)은 압축 없이 파형을 그대로 저장하는 방식이라 음질 손실이 없고 재생할 때 디코딩도 필요 없지만, 용량은 줄지 않으므로 짧은 효과음 정도에만 사용합니다.

코덱 선택과 별개로, 소스 파일은 무손실 WAV로 넣는 편이 일반적입니다. MP3처럼 이미 손실 압축을 거친 파일을 소스로 넣으면, 한 번 손실된 데이터에 Unity가 Vorbis 같은 손실 압축을 다시 적용해 음질이 이중으로 떨어지기 때문입니다.

### Load Type: 메모리와 CPU의 트레이드오프

**Load Type**은 임포트한 오디오 데이터를 런타임에 어떤 형태로 메모리에 올려 둘지 정하는 설정입니다. 같은 코덱으로 압축한 파일이라도 압축을 미리 풀어 둘지, 재생하면서 풀지에 따라 메모리와 CPU의 균형점이 달라집니다.

<br>

**Load Type 비교**

| Load Type | 메모리 | CPU 비용 | 지연시간 |
|---|---|---|---|
| Decompress On Load (로드 시 전부 압축 해제) | 높음 (PCM 크기) | 낮음 (재생 즉시) | 로딩 시 큼 |
| Compressed In Memory (압축 상태로 메모리 보관) | 낮음 (압축 크기) | 중간 (실시간 디코딩) | 재생 시 약간 |
| Streaming (디스크에서 실시간 읽기) | 최소 (버퍼만) | 높음 (디스크 + 디코딩) | 재생 시 약간 |

<br>

표 첫 줄의 **Decompress On Load**는 메모리에 올릴 때 파일 전체를 PCM으로 압축 해제합니다. 디코딩을 로드 시점에 미리 끝내 두므로, 재생할 때는 별도의 처리가 필요 없어 지연이 작습니다. 대신 압축을 푼 뒤의 PCM 크기만큼 메모리를 사용합니다. 1분짜리 스테레오 44.1kHz 16비트 오디오라면 약 10MB가 필요한데, 초당 샘플 44,100개에 2채널, 샘플당 2바이트, 60초를 곱한 값입니다. 발소리, 타격음, 버튼 클릭처럼 짧고 즉각 들려야 하는 효과음에 잘 맞습니다.

이 메모리 부담을 줄이려면, 데이터를 압축된 상태 그대로 보관하는 **Compressed In Memory**를 선택할 수 있습니다. 메모리는 압축된 크기만큼만 사용하는 대신 재생할 때마다 CPU가 실시간으로 디코딩하므로, 같은 사운드가 동시에 여러 번 재생되면 CPU 부하도 함께 올라갑니다. 따라서 대사나 내레이션 같은 중간 길이 음성이나, 자주 재생되지 않는 효과음에 적합합니다.

BGM이나 환경음처럼 몇 분씩 이어지는 오디오는 전체를 올려 두면 그만큼 메모리를 오래 차지하지만, 재생은 앞에서부터 차례로 진행되므로 한 번에 필요한 데이터는 그중 일부에 그칩니다. **Streaming**은 오디오 전체를 메모리에 올리지 않고, 재생 중에 디스크에서 필요한 구간을 조금씩 읽습니다. 메모리에는 작은 재생 버퍼만 남는 대신, 디스크 읽기와 디코딩이 재생 내내 이어집니다. 동시에 스트리밍하는 오디오가 많아지면 디스크 읽기가 겹쳐 서로 늦어지므로, 모바일에서는 동시 스트리밍 수를 1~2개 정도로 제한하는 편이 일반적입니다.

### Preload Audio Data

**Preload Audio Data**는 오디오 데이터를 언제 메모리에 로드할지를 정하는 설정입니다. 켜 두면 해당 오디오가 포함된 씬을 불러올 때 오디오 데이터도 함께 로드됩니다. 꺼 두면 첫 재생 시점까지 로드가 미뤄지며, 그만큼 첫 재생에서 짧은 지연이 생길 수 있습니다.

따라서 입력 직후 재생되어야 하는 효과음은 Preload를 켜 두는 것이 안전합니다. 반면 재생 시점이 늦은 BGM이나 컷씬 음성은 꺼 두면 씬 진입 때 미리 올릴 데이터가 적어져, 초기 로딩 시간을 줄일 수 있습니다.

### 모바일에서의 권장 설정

모바일에서는 메모리와 CPU 제약이 모두 크므로, 모든 사운드를 한 가지 설정으로 묶기보다 오디오 성격에 따라 Load Type과 코덱을 나눠 적용하는 편이 효율적입니다. 길이와 재생 빈도를 기준으로 정리하면 다음과 같습니다.

<br>

**모바일 오디오 권장 설정**

| 오디오 유형 | Load Type | 코덱 |
|---|---|---|
| 짧은 효과음 (< 1초) | Decompress On Load | ADPCM 또는 PCM |
| 중간 효과음/음성 (1~10초) | Compressed In Memory | Vorbis (Quality 70%) |
| BGM/환경음 (> 10초) | Streaming | Vorbis (Quality 50~70%) |

표의 Load Type과 코덱을 정하고 나면, 데이터량 자체를 줄이는 두 설정을 함께 조정할 수 있습니다. **Force Mono**를 켜면 스테레오 오디오가 모노로 합쳐져 채널이 둘에서 하나로 줄고, 채널 수가 절반이 되는 만큼 메모리도 절반으로 줄어듭니다. 모바일 스피커로는 좌우 분리감이 거의 느껴지지 않는 효과음이 많으므로, 그런 효과음에 적용하면 체감 음질 손실을 크게 만들지 않고 용량을 절약할 수 있습니다.

**Sample Rate**는 1초의 소리를 몇 개의 샘플로 표현할지를 정합니다. 44,100Hz를 22,050Hz로 낮추면 초당 샘플 수가 절반이 되어 데이터량도 줄어듭니다. 짧은 효과음은 22,050Hz로도 충분한 경우가 많지만, 음질 차이가 쉽게 느껴지는 BGM은 원본 스테레오와 44,100Hz를 그대로 유지하는 것이 좋습니다.

---

## Import Settings가 빌드 크기와 메모리에 미치는 영향

Import Settings는 에디터 안에서만 쓰이는 설정이 아닙니다. 텍스처, 모델, 오디오가 어떤 해상도와 압축 방식, 로드 방식으로 변환되는지를 정하고, 그 결과가 빌드 파일의 크기와 런타임 메모리 사용량으로 이어집니다.

그중 가장 먼저 확인할 대상은 보통 텍스처입니다. 텍스처는 개수가 많고 해상도가 커지기 쉬우며, GPU가 사용할 수 있는 포맷으로 변환된 뒤에도 많은 메모리를 차지합니다. 같은 2048x2048 이미지라도 ASTC, ETC2, 비압축 RGBA처럼 어떤 포맷으로 임포트하느냐에 따라 빌드 크기와 메모리 사용량이 크게 달라집니다.

프로젝트마다 비중은 다르지만, 모바일 게임에서는 Build Report나 Memory Profiler에서 텍스처 영역이 가장 크게 보이는 경우가 많습니다. 따라서 빌드 크기나 메모리 사용량을 줄이려면 먼저 텍스처의 압축 포맷, Max Size, 밉맵 설정을 확인하고, 그다음 모델과 오디오 설정을 함께 조정하는 흐름이 좋습니다.

### 텍스처 압축 포맷 비교

압축 포맷은 텍스처 메모리를 볼 때 가장 먼저 확인할 축입니다. 같은 해상도라면, 한 픽셀을 몇 비트로 저장하느냐에 따라 필요한 메모리가 거의 그대로 결정됩니다. 이 기준이 **bpp(bits per pixel)**이며, 말 그대로 한 픽셀이 차지하는 비트 수를 뜻합니다.

ASTC 포맷 뒤에 붙는 4x4, 6x6, 8x8 같은 숫자는 압축 블록 하나가 담당하는 픽셀 영역입니다. ASTC는 블록 크기가 달라도 블록 하나를 항상 128비트(16바이트)로 저장합니다. 따라서 4x4 블록은 16픽셀을 128비트에 담고, 6x6 블록은 36픽셀을 같은 128비트에 담습니다.

이 차이 때문에 품질과 용량의 트레이드오프가 생깁니다. 블록이 클수록 같은 128비트로 더 많은 픽셀을 표현하므로 bpp가 낮아지고 메모리는 줄어듭니다. 대신 한 블록 안에서 표현할 수 있는 색상 정보가 상대적으로 줄어들어, 그라데이션이나 노멀맵처럼 변화가 섬세한 텍스처에서는 압축 아티팩트가 더 잘 보일 수 있습니다.

아래 표는 2048x2048 텍스처 한 장이 각 포맷으로 GPU 메모리에 올라갔을 때의 대략적인 크기입니다. 밉맵 포함 값은 전체 밉 체인을 함께 저장한다고 보고 계산한 값입니다.

**2048 x 2048 텍스처 포맷별 메모리 비교**

| 포맷 | bpp | 메모리 (밉맵 제외) | 메모리 (밉맵 포함) |
|---|---|---|---|
| RGBA32 | 32 | 16 MB | 21.3 MB |
| RGBA16 | 16 | 8 MB | 10.6 MB |
| BC7 (PC) | 8 | 4 MB | 5.3 MB |
| ASTC 4x4 | 8 | 4 MB | 5.3 MB |
| ASTC 6x6 | 3.56 | 1.78 MB | 2.37 MB |
| ASTC 8x8 | 2 | 1 MB | 1.33 MB |
| ETC2 (RGB / RGBA) | 4 / 8 | 2 / 4 MB | 2.7 / 5.3 MB |

ETC2는 알파 채널 사용 여부에 따라 bpp가 달라집니다. RGB만 저장하면 4bpp이고, 알파 채널까지 포함하면 8bpp로 올라갑니다. ASTC도 블록 크기에 따라 bpp가 달라지며, 표에서 보듯 ASTC 6x6은 무압축 RGBA32와 비교해 약 1/9 정도의 메모리만 사용합니다.

밉맵도 함께 봐야 합니다. 밉맵을 켜면 원본보다 작은 단계의 텍스처들이 추가로 저장되므로, 전체 메모리는 보통 약 33% 늘어납니다. 그래서 압축 포맷을 비교할 때는 밉맵을 켤 텍스처인지, UI처럼 한 해상도로만 쓸 텍스처인지도 함께 판단해야 합니다.

이 차이를 프로젝트 단위로 확대하면 영향이 더 분명해집니다. 2048x2048 텍스처 100장이 모두 메모리에 올라와 있다고 가정하면, RGBA32는 밉맵을 제외해도 약 1.6GB가 필요합니다. 같은 텍스처를 ASTC 6x6으로 임포트하면 약 178MB 수준으로 줄어듭니다. 모바일 기기처럼 메모리 여유가 제한적인 환경에서는 이런 차이가 OOM(Out Of Memory) 발생 여부로 이어질 수 있습니다.

### Max Size와 밉맵 유무의 영향

압축 포맷이 한 픽셀의 크기를 정한다면, **Max Size**는 텍스처가 사용할 최대 해상도를 정합니다. 같은 ASTC 6x6 포맷이라도 Max Size를 낮추면 실제로 저장되는 픽셀 수가 줄어들고, 그만큼 메모리도 줄어듭니다.

여기에 밉맵 생성 여부가 다시 영향을 줍니다. 밉맵을 켜면 원본 텍스처보다 작은 해상도 단계들이 함께 만들어지므로 메모리를 더 사용합니다. 2048x2048 ASTC 6x6 텍스처 한 장을 기준으로 Max Size와 밉맵 설정에 따른 메모리 변화를 보면 다음과 같습니다.

<br>

**Max Size와 밉맵 조합별 메모리** (ASTC 6x6 기준)

| Max Size | 밉맵 OFF | 밉맵 ON |
|---|---|---|
| 2048 | 1.78 MB | 2.37 MB |
| 1024 | 0.44 MB | 0.59 MB |
| 512 | 0.11 MB | 0.15 MB |
| 256 | 0.03 MB | 0.04 MB |

Max Size를 2048에서 1024로 낮추면 가로와 세로가 각각 절반이 됩니다. 텍스처 메모리는 면적에 비례하므로, 픽셀 수는 1/4로 줄고 메모리도 같은 비율로 줄어듭니다. 큰 텍스처일수록 Max Size 한 단계가 만드는 차이가 큽니다.

밉맵은 반대로 메모리를 더 쓰는 설정입니다. 전체 밉 체인을 저장하면 보통 원본 텍스처 대비 약 33%의 메모리가 추가됩니다. 다만 3D 오브젝트처럼 카메라와의 거리에 따라 화면에서 크기가 계속 바뀌는 텍스처는 밉맵을 끄기 어렵습니다. 멀리 있는 오브젝트가 작은 화면 영역에 그려질 때 적절한 낮은 해상도 단계를 쓰지 못하면, 계단 현상이나 깜빡임 같은 앨리어싱이 더 잘 보입니다.

반면 UI처럼 화면에 고정된 크기로 그려지는 텍스처는 카메라 거리 때문에 작아지는 일이 거의 없습니다. 이런 텍스처는 밉맵을 꺼 두는 편이 메모리 측면에서 유리합니다.

최적화할 때는 전체 텍스처를 한꺼번에 낮추기보다, Memory Profiler나 빌드 리포트에서 메모리 사용량이 큰 텍스처부터 확인하는 편이 좋습니다. 먼저 압축 포맷과 Max Size를 보고, 그 텍스처가 3D 표면용인지 UI용인지에 따라 밉맵 필요 여부를 결정합니다.

---

## AssetPostprocessor

효과적인 Import Settings를 알아도, 에셋이 수백 개로 늘어난 프로젝트에서 이를 하나씩 손으로 적용하기는 어렵습니다. 팀 프로젝트라면 같은 종류의 에셋인데도 작업자마다 설정이 달라지는 문제도 생깁니다. Unity는 이런 반복과 편차를 줄일 수 있도록 **AssetPostprocessor**를 제공합니다.

**AssetPostprocessor**는 에셋 임포트 과정에 개입하는 에디터 전용 클래스입니다. `OnPreprocessTexture`, `OnPreprocessModel`, `OnPreprocessAudio` 같은 메서드를 구현하면, Unity가 변환을 시작하기 전에 Import Settings를 코드로 지정할 수 있습니다. 변환이 끝난 뒤에는 `OnPostprocessTexture`, `OnPostprocessModel` 같은 메서드가 호출되므로, 결과물을 검사하거나 추가 처리를 적용할 때는 이 후처리 콜백을 사용합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 380 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 380px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="190" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">AssetPostprocessor 동작 흐름</text>
  <!-- Step 1 -->
  <rect x="65" y="32" width="250" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="190" y="55" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">에셋 임포트 시작</text>
  <!-- Arrow 1→2 -->
  <line x1="190" y1="68" x2="190" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="190,94 186,86 194,86" fill="currentColor"/>
  <!-- Step 2 -->
  <rect x="65" y="96" width="250" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="190" y="116" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">OnPreprocessXXX 호출</text>
  <text fill="currentColor" x="190" y="133" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">Import Settings를 코드로 설정</text>
  <!-- Arrow 2→3 -->
  <line x1="190" y1="144" x2="190" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="190,166 186,158 194,158" fill="currentColor"/>
  <!-- Step 3 -->
  <rect x="65" y="168" width="250" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="190" y="191" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Unity 임포트 엔진이 변환 수행</text>
  <!-- Arrow 3→4 -->
  <line x1="190" y1="204" x2="190" y2="220" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="190,226 186,218 194,218" fill="currentColor"/>
  <!-- Step 4 -->
  <rect x="65" y="228" width="250" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="190" y="248" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">OnPostprocessXXX 호출</text>
  <text fill="currentColor" x="190" y="265" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">임포트 결과를 후처리</text>
  <!-- Arrow 4→5 -->
  <line x1="190" y1="276" x2="190" y2="292" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="190,298 186,290 194,290" fill="currentColor"/>
  <!-- Step 5 -->
  <rect x="65" y="300" width="250" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="190" y="323" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">임포트 완료, Library에 캐싱</text>
</svg>
</div>

<br>

팀에서 공통으로 적용할 Import Settings는 전처리 단계에 두는 편이 적절합니다. Unity가 실제 변환을 시작하기 전에 설정을 확정하므로, 작업자가 에셋을 추가하거나 다시 임포트해도 같은 규칙이 반복해서 적용됩니다.

아래 예시는 `OnPreprocessTexture`에서 텍스처의 폴더 경로를 기준으로 설정을 나누는 방식입니다. UI 텍스처는 작은 Max Size와 밉맵 비활성화를 적용하고, 캐릭터 텍스처는 더 큰 Max Size와 밉맵 사용을 허용하는 식으로 용도별 규칙을 코드에 모아 둡니다.

```csharp
using UnityEditor;
using UnityEngine;

public class TextureImportRule : AssetPostprocessor
{
    void OnPreprocessTexture()
    {
        var importer = (TextureImporter)assetImporter;

        if (assetPath.Contains("Assets/Art/UI/"))
        {
            importer.maxTextureSize = 512;
            importer.textureCompression = TextureImporterCompression.Compressed;
            importer.mipmapEnabled = false; // UI는 밉맵 불필요
        }
        else if (assetPath.Contains("Assets/Art/Characters/"))
        {
            importer.maxTextureSize = 1024;
            importer.textureCompression = TextureImporterCompression.Compressed;
            importer.mipmapEnabled = true;
        }
        else if (assetPath.Contains("Assets/Art/Background/"))
        {
            importer.maxTextureSize = 512;
            importer.textureCompression = TextureImporterCompression.Compressed;
            importer.mipmapEnabled = true;
        }
    }
}
```

<br>

이런 스크립트는 에디터 전용 코드로 분리해야 합니다. `AssetPostprocessor`와 `TextureImporter`는 `UnityEditor` 네임스페이스에 속하므로 플레이어 빌드에 포함될 수 없습니다. 일반적으로는 `Editor` 폴더 아래에 두고, asmdef를 사용하는 프로젝트라면 Editor 전용 Assembly Definition으로 분리합니다. 그렇지 않으면 플레이어 빌드 컴파일 단계에서 `UnityEditor`를 찾지 못해 오류가 발생할 수 있습니다.

에디터 전용으로 분리된 `AssetPostprocessor`는 에셋이 임포트될 때만 동작합니다. 이후 `Assets/Art` 아래에 텍스처를 새로 추가하거나 기존 텍스처를 다시 임포트하면, Unity는 실제 변환 전에 위 규칙을 적용합니다. 작업자가 Inspector에서 같은 설정을 반복해서 맞추지 않아도, 폴더 구조를 기준으로 Import Settings가 일정하게 유지됩니다.

같은 방식으로 다른 에셋 유형의 규칙도 코드화할 수 있습니다. 모델은 `OnPreprocessModel`에서 Read/Write Enabled, 메시 압축, 최적화 옵션을 정할 수 있고, 오디오는 `OnPreprocessAudio`에서 Load Type이나 압축 품질을 용도별로 고정할 수 있습니다. 이렇게 에셋 종류별 규칙을 임포트 단계에 두면, 수동 설정에서 생기는 편차를 줄일 수 있습니다.

다만 규칙이 여러 스크립트로 나뉘어 있으면 실행 순서가 문제가 될 수 있습니다. 둘 이상의 `AssetPostprocessor`가 같은 에셋의 같은 설정을 수정하면, 나중에 실행된 쪽이 앞선 설정을 덮어씁니다. 순서가 의미 있는 규칙은 가능한 한 한 곳에서 관리하고, 분리해야 한다면 `GetPostprocessOrder()`를 오버라이드해 실행 순서를 명시합니다.

---

## 마무리

이번 글에서는 소스 에셋이 임포트를 거쳐 엔진용 데이터로 변환되는 과정과, 그 변환을 정하는 Import Settings가 어떤 비용을 결정하는지 살펴보았습니다. 핵심은 다음과 같습니다.

- **Asset Import Pipeline**은 소스 에셋을 엔진이 사용할 수 있는 임포트 에셋으로 변환하고, 결과물을 Library 폴더에 캐싱합니다. 이때 어떤 설정으로 변환하느냐가 결과물의 비용과 품질을 정합니다.
- **`.meta` 파일**은 에셋의 GUID와 Import Settings를 저장합니다. Library 폴더는 다시 만들 수 있지만, `.meta` 파일을 잃으면 GUID가 새로 만들어져 기존 참조가 끊어지므로 버전 관리에 반드시 포함해야 합니다.
- **텍스처**는 압축 포맷과 Max Size가 메모리 사용량을 좌우합니다. Read/Write Enabled를 켜면 같은 데이터가 GPU 메모리와 CPU 메모리에 각각 유지되어, 사용량이 두 배가 됩니다.
- **모델**은 Mesh Compression이 빌드 파일 크기만 줄이고 런타임 메모리는 줄이지 않습니다. Optimize Mesh는 캐시 히트율을 높여 정점의 중복 변환을 줄이므로, 정점 인덱스에 의존하는 코드가 없다면 켜 두는 것이 좋습니다.
- **오디오**는 코덱이 저장 크기를, Load Type이 메모리와 CPU 비용의 균형점을 정합니다. 짧은 효과음은 Decompress On Load, 중간 길이 음성은 Compressed In Memory, BGM은 Streaming이 기본 기준입니다.
- **AssetPostprocessor**를 사용하면 Import Settings를 코드로 강제할 수 있습니다. 폴더 구조에 규칙을 연결해 두면, 팀 전체의 에셋 설정이 일관되게 유지됩니다.

정리하면, Import Settings는 빌드 크기와 메모리 사용량, 품질 사이의 균형을 정하는 지점입니다. 같은 2048x2048 텍스처 100장도 압축 포맷에 따라 약 1.6GB를 차지하기도, 178MB에 그치기도 합니다. 텍스처와 오디오처럼 수가 많고 용량이 큰 에셋일수록, 이 설정 차이가 프로젝트 전체 비용으로 이어집니다.

여기까지가 에셋이 프로젝트에 들어와 엔진용 데이터로 준비되는 임포트 단계입니다. 다음 글에서는 이렇게 만들어진 에셋 데이터가 디스크에 **직렬화(Serialization)**된 형태로 저장되고 런타임에 역직렬화되어 메모리에 올라오는 흐름을 다루고, `Instantiate`가 에셋을 실제 오브젝트 인스턴스로 복제하는 과정도 함께 살펴봅니다.

[Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)에서 이 흐름을 이어갑니다. 에셋 메모리를 실제로 관리하는 방식은 [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 다룹니다.

<br>

---

**관련 글**
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)

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
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱](/dev/unity/RasterPipeline-3/)
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)
- [Unity 엔진 핵심 (3) - Unity 실행 순서](/dev/unity/UnityCore-3/)
- [Unity 엔진 핵심 (4) - Unity의 스레딩 모델](/dev/unity/UnityCore-4/)
- **Unity 에셋 시스템 (1) - Asset Import Pipeline** (현재 글)
- [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)
- [Unity 에셋 시스템 (3) - Scene Management](/dev/unity/UnityAsset-3/)
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
