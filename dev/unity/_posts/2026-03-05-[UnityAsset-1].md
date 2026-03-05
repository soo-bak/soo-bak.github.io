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

[메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 텍스처, 메쉬, 오디오 등의 에셋이 네이티브 메모리의 대부분을 차지한다는 점을 다루었고, [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서는 텍스처의 압축 포맷과 메모리 계산 방법을 다루었습니다. 두 글 모두 에셋이 이미 엔진 내부에 로드된 상태를 전제로 설명하고 있습니다.

하지만 같은 PSD 파일이라도 임포트 설정에 따라 4MB 텍스처가 될 수도 있고, 40MB 텍스처가 될 수도 있습니다. 메모리 최적화의 출발점은 에셋이 메모리에 올라가기 전 단계 — 임포트 과정입니다.

프로젝트가 커지면서 에셋이 수백, 수천 개로 늘어나면 임포트 설정의 영향이 누적됩니다. 아티스트가 작업한 4096×4096 PSD 파일이 기본 설정 그대로 임포트되거나, 1분짜리 BGM이 무압축으로 약 10MB의 메모리를 차지하는 상황은 모바일 프로젝트에서 흔히 발생합니다.

<br>

Photoshop의 PSD 파일이나 Maya의 FBX 파일은 그 자체로는 Unity 엔진이 직접 사용할 수 없습니다. **Asset Import Pipeline**은 이 원본 파일을 엔진 내부 포맷으로 변환하고, 변환 결과물을 캐싱하는 전체 과정입니다. 변환 과정에서 어떤 설정을 적용하느냐에 따라 빌드 크기, 메모리 사용량, 로딩 속도가 달라집니다.

이 글에서는 소스 에셋과 임포트 에셋의 차이, Library 폴더의 역할, 텍스처·모델·오디오 각각의 임포트 과정, 그리고 Import Settings가 빌드에 미치는 영향을 살펴봅니다.

---

## 소스 에셋 vs 임포트 에셋

Unity 프로젝트의 에셋은 **소스 에셋(Source Asset)**과 **임포트 에셋(Imported Asset)** 두 형태로 관리됩니다. 소스 에셋은 작업 도구가 생성한 원본이고, 임포트 에셋은 그 원본을 엔진이 실제로 사용할 수 있는 포맷으로 변환한 결과물입니다.

소스 에셋은 Photoshop의 PSD, Maya/Blender의 FBX, Audacity의 WAV처럼 작업 도구에서 만든 원본 파일로, Unity 프로젝트의 `Assets` 폴더에 저장됩니다. 아티스트와 사운드 디자이너가 직접 수정하는 대상이므로 Git 등 버전 관리에 포함합니다.

앞서 살펴본 것처럼 PSD나 FBX는 런타임에서 그대로 사용할 수 없으므로, Unity는 PSD를 ASTC 같은 GPU 압축 텍스처로, FBX를 내부 메쉬 포맷으로 변환합니다. 이렇게 변환된 임포트 에셋이 엔진이 실제로 읽는 데이터입니다. 변환 결과물은 프로젝트의 `Library` 폴더에 캐싱됩니다.

<br>

<div style="text-align: center;">
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

소스 에셋을 Assets 폴더에 넣으면 Unity 에디터가 자동으로 감지하여 임포트를 수행합니다. 이때 적용되는 설정이 에셋의 **Import Settings**입니다. Import Settings에는 최종 해상도(Max Size), 압축 포맷, 밉맵 생성 여부 등이 포함되며, 이 설정의 조합이 임포트 결과물의 메모리 크기와 품질을 결정합니다.

### .meta 파일

소스 에셋마다 `.meta` 파일이 함께 생성됩니다. `.meta` 파일에는 해당 에셋의 **GUID(Globally Unique Identifier)**와 **Import Settings**가 저장됩니다. GUID는 프로젝트 전체에서 에셋을 유일하게 식별하는 문자열입니다.

<br>

<div style="text-align: center;">
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

Unity는 에셋 간 참조를 파일 경로가 아니라 GUID로 관리합니다. 예를 들어 머티리얼이 텍스처를 참조할 때, 내부적으로는 텍스처의 GUID를 기록합니다. 파일 이름이나 경로를 변경해도 GUID가 유지되면 참조가 깨지지 않습니다.

반대로, `.meta` 파일을 삭제하면 Unity가 새로운 GUID를 생성하므로 기존 참조가 모두 깨집니다. 에셋을 이동하거나 이름을 변경할 때는 반드시 Unity 에디터 안에서(Project 창에서) 수행해야 `.meta` 파일이 함께 갱신됩니다. OS의 파일 탐색기에서 직접 옮기면 `.meta` 파일이 분리될 수 있습니다. `.meta` 파일은 반드시 버전 관리에 포함해야 합니다.

---

## Library 폴더 — 임포트 캐시

`Library` 폴더는 임포트 결과물이 저장되는 로컬 캐시입니다. Unity가 소스 에셋을 임포트할 때마다 변환 결과가 이 폴더에 기록됩니다.

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

Library 폴더는 **재생성이 가능합니다.** Library 폴더를 삭제해도 Unity 에디터를 다시 열면 Assets 폴더의 소스 에셋과 `.meta` 파일을 기반으로 전체 임포트를 다시 수행합니다. 다만 프로젝트 규모에 따라 수 분에서 수십 분이 소요될 수 있습니다. 팀 환경에서는 **Unity Accelerator**(캐시 서버)로 이 재임포트 비용을 줄일 수 있습니다. Unity Accelerator는 팀원이 이미 생성한 임포트 결과물을 네트워크로 공유하여, 다른 팀원이 같은 에셋을 처음부터 임포트하지 않아도 되게 합니다.

이처럼 재생성이 가능하므로 Library 폴더는 **버전 관리에서 제외합니다.** `.gitignore`에 `Library/`를 추가하는 것이 표준적인 관행입니다.

Library 폴더에는 **플랫폼별 변환 결과**가 저장됩니다. Android 플랫폼으로 전환하면 텍스처가 ASTC(Adaptive Scalable Texture Compression)나 ETC2(Ericsson Texture Compression 2) 같은 GPU 압축 포맷으로 변환되고, iOS 플랫폼으로 전환하면 ASTC로 변환됩니다. 플랫폼을 전환할 때마다 임포트 캐시가 갱신되며, 플랫폼 전환(Switch Platform)에 시간이 오래 걸리는 것은 이 재변환 때문입니다.

### Artifact 구조와 Asset Pipeline v2

**Artifact**는 하나의 소스 에셋을 특정 Import Settings·Unity 버전·플랫폼 조합으로 임포트한 결과물입니다. 소스 에셋의 GUID, Import Settings, Unity 버전, 플랫폼 — 이 네 조건 중 하나라도 바뀌면 해당 Artifact가 다시 생성됩니다.

<br>

<div><svg viewBox="0 0 480 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
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

Unity 2019.3부터 도입된 **Asset Pipeline v2**는 이 Artifact 시스템을 개선하여, 변경된 에셋만 선택적으로 재임포트하고 임포트 결과를 결정론적(deterministic)으로 생성합니다. 소스 에셋과 Import Settings가 동일하면 어느 컴퓨터에서든 항상 같은 임포트 결과가 나오므로, 팀원들이 각자의 로컬 Library 폴더에서 독립적으로 임포트하더라도 동일한 빌드를 생성할 수 있습니다.

---

## 텍스처 임포트

텍스처는 Unity 프로젝트에서 가장 큰 용량을 차지하는 에셋 유형입니다. 임포트 과정에서 적용하는 설정이 메모리와 빌드 크기에 직접적인 영향을 미칩니다.

### 소스 포맷에서 엔진 포맷으로

PNG, PSD, TGA, EXR 등의 소스 파일은 임포트 과정에서 플랫폼별 GPU 압축 포맷으로 변환됩니다.

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

소스 파일의 포맷(PNG인지 PSD인지)은 임포트 결과에 영향을 주지 않습니다. Unity는 소스 파일에서 픽셀 데이터만 읽어 Import Settings에 따라 변환하며, PSD 파일의 레이어 구조처럼 픽셀 데이터 외의 정보는 무시합니다. 따라서 소스 파일의 포맷은 아티스트의 작업 편의성에 맞추면 됩니다.

### 텍스처 유형 설정

Import Settings의 **Texture Type**은 Unity가 텍스처를 어떤 용도로 사용할지 지정합니다. Texture Type에 따라 sRGB 감마 보정 적용 여부, 압축 포맷 선택, 픽셀 값의 해석 방식이 달라집니다.

<br>

**주요 Texture Type**

| Texture Type | 특성 |
|---|---|
| Default | 일반 색상 텍스처. Diffuse, Albedo, Emission 등에 사용. sRGB 감마 보정 기본 적용. |
| Normal Map | 법선 맵 전용. 픽셀 값을 방향 벡터로 해석. sRGB 끔. 압축 시 전용 포맷 사용. |
| Sprite (2D/UI) | 2D 스프라이트 및 UI용. Sprite Editor에서 슬라이싱 가능. 아틀라스 패킹 대상. |
| Single Channel | 마스크, 하이트맵 등 1채널 데이터 전용. R 또는 Alpha 채널만 사용하여 메모리 절약. |

이 밖에 Cursor(커서 이미지), Cookie(라이트 쿠키), Lightmap(HDR 인코딩 라이트맵) 등 특수 용도 타입이 있습니다.

<br>

Texture Type을 잘못 설정하면 렌더링이 왜곡되거나 메모리가 낭비됩니다. Normal Map용 텍스처를 Default로 임포트하면 sRGB 감마 보정이 적용되어, 방향 벡터로 해석해야 할 수치 데이터에 감마 디코딩이 가해지므로 법선 방향이 왜곡됩니다. 마스크 텍스처에 Single Channel 대신 Default를 사용하면 불필요한 RGB 채널까지 저장되어 메모리가 낭비됩니다. UI 텍스처는 Sprite (2D/UI) 타입으로 지정해야 슬라이싱과 아틀라스 패킹을 사용할 수 있습니다.

### Max Size — 메모리와 품질의 핵심 설정

**Max Size**는 임포트 결과 텍스처의 최대 해상도를 제한합니다. 소스 파일이 4096x4096이더라도 Max Size를 1024로 설정하면, 임포트 결과는 1024x1024가 됩니다.

<br>

**Max Size에 따른 메모리 변화** (ASTC 6x6 기준, 밉맵 포함, 소스: 4096 x 4096)

| Max Size | 해상도 | 메모리 (약) |
|---|---|---|
| 4096 | 4096 x 4096 | 9.5 MB |
| 2048 | 2048 x 2048 | 2.37 MB |
| 1024 | 1024 x 1024 | 0.59 MB |
| 512 | 512 x 512 | 0.15 MB |
| 256 | 256 x 256 | 0.04 MB |

Max Size를 한 단계 낮출 때마다 가로·세로 해상도가 각각 절반이 되어 전체 픽셀 수가 1/4로 줄고, 메모리도 약 1/4로 감소합니다.

<br>

모바일 프로젝트에서는 텍스처의 시각적 중요도에 따라 Max Size를 다르게 설정합니다. 화면에 크게 보이는 캐릭터 텍스처는 2048, 먼 배경 오브젝트는 512, UI 아이콘은 256과 같은 식으로 차등 적용합니다. Max Size를 시각적 중요도에 맞게 차등 관리하면 텍스처 메모리를 크게 줄일 수 있습니다.

### sRGB vs Linear

사람의 눈은 어두운 영역의 밝기 변화에 민감한 반면, 밝은 영역에서는 둔감합니다. 8비트(256단계)로 밝기를 표현할 때, 이 단계를 물리적 밝기에 균등하게 대응시키면 눈이 민감한 어두운 영역에서 단계 간 차이가 두드러져 색 띠(banding)가 나타납니다. **sRGB**는 어두운 영역에 더 많은 단계를 할당하는 비선형 변환(**감마 인코딩**)을 적용하여 이 문제를 줄이는 색상 공간이며, 디지털 이미지 대부분이 이 방식으로 저장됩니다.

<br>

sRGB가 저장에 효율적인 반면, 셰이더의 조명 연산은 선형(Linear) 공간에서 수행해야 합니다. 물리 세계에서 빛의 세기는 선형적으로 합산되므로, 감마 인코딩된 값으로 조명을 계산하면 결과가 왜곡됩니다. sRGB를 켜면 GPU가 텍스처 샘플링 시 감마 인코딩된 값을 선형 공간으로 자동 변환하여 셰이더에 전달합니다.

색상 정보를 담는 텍스처(Diffuse, Albedo)는 감마 인코딩된 상태로 저장되어 있으므로, sRGB를 켜서 선형 공간으로 변환한 뒤 셰이더에 전달해야 합니다. 수치 데이터를 담는 텍스처(Normal Map, Mask, Height Map)는 sRGB를 꺼야 합니다. 이 텍스처들은 색상이 아니라 방향 벡터나 높이 같은 수치를 저장하고 있으므로, 감마 디코딩을 적용하면 값이 왜곡됩니다.

### Read/Write Enabled의 비용

**Read/Write Enabled**를 켜면 텍스처 데이터를 CPU에서 읽고 쓸 수 있게 됩니다. `Texture2D.GetPixel()`, `Texture2D.SetPixel()` 같은 API를 사용하려면 이 옵션이 필요합니다.

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

Read/Write Enabled가 켜져 있으면, Unity는 GPU에 업로드한 텍스처 데이터의 사본을 CPU 메모리에도 유지합니다. 2048x2048 RGBA32 텍스처라면 16MB가 GPU와 CPU에 각각 올라가 총 32MB를 차지합니다. CPU에서 텍스처 픽셀을 읽거나 수정할 필요가 없다면, 반드시 이 옵션을 꺼야 합니다.

### Mipmap 생성

**Generate Mip Maps**를 켜면 원본 텍스처를 절반씩 축소한 여러 단계의 이미지 체인이 생성됩니다. 밉맵(Mipmap)의 MIP는 라틴어 "multum in parvo(작은 공간에 많은 것)"의 약자입니다.

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

3D 오브젝트에 사용하는 텍스처에는 밉맵을 켜는 것이 일반적입니다. 카메라에서 멀리 있는 오브젝트는 화면에서 작은 영역을 차지합니다. 예를 들어 1024×1024 텍스처가 화면에서 4×4 픽셀로 표시되는 경우, 밉맵이 없으면 GPU는 원본의 약 100만 텍셀(texel, 텍스처를 구성하는 개별 픽셀)을 읽어 단 16픽셀로 축소해야 하므로 메모리 대역폭이 낭비됩니다. 밉맵이 있으면 GPU가 화면 크기에 맞는 축소된 밉 레벨을 선택하여 읽어야 할 데이터량을 줄입니다.

밉맵은 앨리어싱 방지에도 필요합니다. 원본 텍스처에 체크무늬나 격자처럼 픽셀이 빠르게 바뀌는 세밀한 패턴(고주파 디테일)이 포함되어 있을 때, 이를 극단적으로 축소하면서 필터링하지 않으면 화면에서 깜빡임(aliasing)이 발생합니다. 밉맵은 각 레벨을 미리 다운샘플링하여 고주파 성분을 사전에 걸러내므로 깜빡임이 줄어듭니다.

UI 텍스처에는 밉맵을 끄는 것이 원칙입니다. UI 요소는 항상 고정된 크기로 렌더링되므로 축소된 밉 레벨이 필요 없고, 밉맵 분량만큼 메모리가 낭비됩니다.

<br>

3D 오브젝트 텍스처에서 밉맵을 켜면 메모리가 33% 증가하지만, Unity 2018.2부터 도입된 **Texture Streaming**(Mipmap Streaming)을 활용하면 이 비용을 줄일 수 있습니다. Texture Streaming은 카메라와의 거리에 따라 필요한 밉 레벨만 메모리에 올리고, 불필요한 고해상도 밉 레벨은 내리는 기능입니다.

Quality Settings의 **Texture Streaming** 항목에서 기능을 활성화한 뒤, 텍스처 Import Settings의 **Streaming Mipmaps** 체크박스를 개별 텍스처마다 켜야 적용됩니다. 메모리 예산(Memory Budget)을 설정하면 Unity가 전체 텍스처의 밉 레벨을 예산 내에서 자동 조절합니다. 3D 오브젝트 텍스처가 많은 프로젝트에서는 밉맵의 렌더링 이점을 유지하면서 메모리 비용을 줄일 수 있습니다.

---

## 모델 임포트

메쉬 데이터는 텍스처와 함께 3D 게임의 시각적 기반을 이룹니다. FBX, OBJ 같은 3D 모델 파일은 임포트 과정에서 Unity의 내부 메쉬 포맷으로 변환됩니다.

### 좌표축 변환과 Scale Factor

3D 작업 도구마다 좌표 체계가 다릅니다. Maya는 오른손 좌표계, Y-up에 센티미터 단위를 사용하고, Blender는 오른손 좌표계, Z-up에 미터 단위, 3ds Max는 오른손 좌표계, Z-up에 인치 또는 센티미터 단위를 사용합니다. Unity는 왼손 좌표계, Y-up에 미터 단위를 사용합니다.

<br>

<div><svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
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

FBX 파일의 기본 단위는 센티미터이므로, Unity는 기본 **Scale Factor 0.01**을 적용하여 미터 단위로 변환합니다. Maya에서 키가 180인 캐릭터를 만들었다면(180cm), Unity에서는 1.8 유닛(1.8m)이 됩니다. Scale Factor를 잘못 설정하면 오브젝트가 100배 크거나 작게 보이는 문제가 발생합니다.

### Mesh Compression

**Mesh Compression** 옵션은 메쉬 데이터를 빌드 파일에 저장할 때의 압축 수준을 설정합니다. Off, Low, Medium, High 네 단계로 나뉘며, 압축 수준이 높을수록 빌드 파일 크기가 줄어듭니다.

다만 압축 수준이 높아지면 정점 좌표의 양자화(quantization) 정밀도가 낮아집니다. 양자화는 연속적인 좌표 값(예: 0.123456)을 제한된 수의 이산 값(예: 0.12)으로 근사하는 처리이며, 이산 값의 간격이 넓을수록 정점 위치가 원래 좌표에서 크게 벗어납니다. 크기가 작은 오브젝트나 정밀한 형태가 중요한 오브젝트에서는 시각적 아티팩트(메쉬 표면이 울퉁불퉁해지거나 가장자리가 어긋나는 현상)가 나타날 수 있으므로, 압축 적용 후 반드시 시각적 변화를 확인합니다.

<br>

<div><svg viewBox="0 0 500 140" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
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

런타임 메모리를 줄이려면 정점 수 자체를 줄이거나 LOD(Level of Detail)를 적용해야 합니다. LOD를 적용하면 카메라와의 거리에 따라 정점 수가 적은 간략화된 메쉬로 자동 교체되므로, 먼 오브젝트에 고해상도 메쉬를 사용하는 낭비를 방지할 수 있습니다.

### Read/Write Enabled (메쉬)

텍스처와 마찬가지로, 메쉬에도 **Read/Write Enabled** 옵션이 있습니다. 이 옵션이 켜져 있으면 메쉬 데이터의 사본이 CPU 메모리에 유지되어 메모리 사용량이 2배가 됩니다. 런타임에 메쉬 정점을 수정하거나(예: 절차적 지형 생성, 피격 시 메쉬 변형), `Mesh.vertices`로 정점 데이터를 읽어야 하는 경우에만 이 옵션을 켭니다. 대부분의 정적 메쉬(배경, 건물, 소품 등)는 런타임 수정이 필요하지 않으므로 반드시 꺼야 합니다.

### Optimize Mesh

**Optimize Mesh** 옵션은 정점(Vertex)과 인덱스(Index)의 순서를 재정렬하여 GPU 캐시 효율을 높입니다.

메쉬는 정점 목록(Vertex Buffer)과 각 삼각형이 어느 정점을 사용하는지 기록한 인덱스 목록(Index Buffer)으로 구성됩니다. 여러 삼각형이 같은 정점을 공유하기 때문에, 같은 정점이 여러 삼각형의 인덱스에서 반복 참조됩니다.

GPU는 정점 셰이더에서 정점을 순차적으로 처리하며, 이미 처리한 정점 결과를 재사용하기 위해 post-transform cache라는 내부 버퍼를 유지합니다. 이 버퍼에 결과가 남아 있으면 같은 정점을 다시 처리하지 않아도 됩니다. 하지만 삼각형을 구성하는 정점들이 메모리상에서 멀리 떨어져 있으면 버퍼에서 결과를 찾지 못해 캐시 누락이 빈번해집니다.

Optimize Mesh를 켜면 Unity가 임포트 시점에 정점 순서를 재배열하여, 공간적으로 가까운 정점이 메모리에서도 인접하게 배치됩니다. 캐시 히트율이 높아져 렌더링 성능이 향상되며, 임포트 시에만 처리 비용이 발생할 뿐 런타임 비용은 없습니다.

다만 정점 인덱스가 재배열되므로, Read/Write Enabled를 켜고 런타임에 `Mesh.vertices[i]`처럼 특정 인덱스로 정점에 접근하는 코드가 있다면 원본 모델과 인덱스 순서가 달라질 수 있습니다. 이런 경우가 아니라면 항상 켜 둡니다.

### Animation 임포트

FBX 파일에 애니메이션 데이터가 포함되어 있으면, Import Settings에 **Rig** 탭과 **Animation** 탭이 나타납니다.

<br>

<div><svg viewBox="0 0 480 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
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
  <text x="130" y="132" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">범용 — 프롭, 동물, 메카닉 등에 적합</text>
  <!-- Humanoid -->
  <text x="44" y="150" font-size="10" font-weight="bold" font-family="monospace" fill="currentColor">Humanoid</text>
  <text x="130" y="150" font-size="10" font-family="sans-serif" fill="currentColor" opacity="0.7">인간형 리깅 — 리타겟팅 가능</text>
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

**Humanoid** 타입은 Unity의 Avatar 시스템을 사용합니다. Avatar 시스템은 인간형 캐릭터의 뼈대 구조를 Unity 내부의 표준 뼈대에 매핑합니다. 이 매핑 덕분에 한 캐릭터용으로 제작된 애니메이션을 다른 캐릭터에게 적용하는 **리타겟팅(Retargeting)**이 가능해집니다. 예를 들어 주인공의 걷기 애니메이션을 NPC에게도 그대로 적용할 수 있습니다.

다만 런타임에 표준 뼈대의 포즈를 캐릭터 고유 뼈대로 변환하는 연산이 매 프레임 발생하여, Generic 대비 CPU 비용이 높습니다. **Generic** 타입은 리타겟팅이 불가능하지만 매핑 과정이 없어 처리 비용이 낮습니다. 인간형 캐릭터가 아닌 오브젝트(문, 차량, 소품 등)에는 Generic을 사용합니다.

---

## 오디오 임포트

텍스처와 모델이 시각적 에셋이라면, 오디오는 청각적 에셋에 해당합니다. 오디오 에셋은 임포트 설정에 따라 메모리 사용량과 CPU 디코딩 비용이 크게 달라집니다. 메모리를 아끼려면 압축률을 높여야 하지만, 그만큼 재생 시 CPU 디코딩 부하가 늘어나므로 코덱과 Load Type 선택이 중요합니다.

### 소스 포맷과 코덱 변환

WAV, MP3, OGG 등의 소스 파일은 임포트 과정에서 Import Settings에서 선택한 코덱으로 변환됩니다.

<br>

<div><svg viewBox="0 0 540 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
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

Unity에서 사용하는 주요 코덱은 세 가지입니다. **Vorbis**는 손실 압축 코덱으로, 높은 압축률에서도 음질 열화가 적어 배경 음악과 긴 효과음에 폭넓게 사용됩니다. **ADPCM**(Adaptive Differential PCM)은 16비트 샘플을 4비트로 인코딩하여 원본 대비 약 3.5~4배 압축하면서도 디코딩 속도가 빠릅니다. 빈번하게 재생되는 짧은 효과음에 적합합니다. **PCM**은 무압축 원본 그대로이며, 음질 손실이 없는 대신 파일 크기가 커서 제한적으로 사용합니다.

소스 파일로는 무손실 WAV를 사용하는 것이 일반적입니다. MP3를 소스로 사용하면, MP3의 손실 압축으로 이미 품질이 떨어진 데이터에 Unity가 Vorbis 등의 손실 압축을 다시 적용하므로 품질이 이중으로 저하됩니다.

### Load Type — 메모리와 CPU의 트레이드오프

오디오의 **Load Type**은 런타임에서 오디오 데이터를 어떻게 메모리에 올리는지 결정합니다.

<br>

**Load Type 비교**

| Load Type | 메모리 | CPU 비용 | 지연시간 |
|---|---|---|---|
| Decompress On Load (로드 시 전부 압축 해제) | 높음 (PCM 크기) | 낮음 (재생 즉시) | 로딩 시 큼 |
| Compressed In Memory (압축 상태로 메모리 보관) | 낮음 (압축 크기) | 중간 (실시간 디코딩) | 재생 시 약간 |
| Streaming (디스크에서 실시간 읽기) | 최소 (버퍼만) | 높음 (디스크 + 디코딩) | 재생 시 약간 |

<br>

**Decompress On Load**는 오디오를 메모리에 로드하는 시점에 전체를 PCM(Pulse Code Modulation)으로 압축 해제합니다. PCM은 오디오 파형을 그대로 샘플 값으로 저장한 무압축 형태입니다. 재생 시 CPU가 디코딩할 필요가 없어 지연이 없지만, 비압축 PCM 크기만큼 메모리를 차지합니다. 1분짜리 스테레오 44.1kHz 16비트 오디오 기준으로 약 10MB입니다(44,100 x 2채널 x 2바이트 x 60초). 짧은 효과음(발소리, 타격음, 버튼 클릭 등)에 적합합니다.

**Compressed In Memory**는 압축된 상태로 메모리에 보관하고, 재생 시 실시간으로 디코딩합니다. 메모리를 절약하지만, 재생할 때마다 CPU에서 디코딩 연산이 발생하며, 동시에 재생되는 사운드가 많으면 CPU 부하도 높아집니다. 중간 길이의 음성(대사, 내레이션)이나 자주 재생되지 않는 효과음에 적합합니다.

**Streaming**은 오디오 데이터를 메모리에 올리지 않고, 재생 시점에 디스크에서 조금씩 읽어옵니다. 메모리 사용량이 가장 적지만(작은 버퍼만 사용), 디스크 I/O와 CPU 디코딩 비용이 모두 발생합니다. 동시에 스트리밍하는 오디오 수가 늘어나면 디스크 I/O 경합이 심해지므로, 모바일에서는 동시 스트리밍 수를 1~2개로 제한하는 것이 일반적입니다. BGM이나 환경음처럼 긴 오디오에 사용합니다.

### Preload Audio Data

**Preload Audio Data**를 켜면, 오디오가 포함된 씬이 로드될 때 오디오 데이터도 함께 로드됩니다. 끄면 첫 재생 시점에 로드되며, 그때 로딩 지연이 발생할 수 있습니다. 즉시 재생해야 하는 효과음은 Preload를 켭니다. 나중에 재생되는 BGM이나 컷씬 음성은 꺼서 초기 로딩 시간을 줄입니다.

### 모바일에서의 권장 설정

모바일 환경에서는 메모리와 CPU 모두 제한적이므로, 오디오 유형별로 Load Type과 코덱을 다르게 적용합니다.

<br>

**모바일 오디오 권장 설정**

| 오디오 유형 | Load Type | 코덱 |
|---|---|---|
| 짧은 효과음 (< 1초) | Decompress On Load | ADPCM 또는 PCM |
| 중간 효과음/음성 (1~10초) | Compressed In Memory | Vorbis (Quality 70%) |
| BGM/환경음 (> 10초) | Streaming | Vorbis (Quality 50~70%) |

Load Type과 코덱 외에 두 가지 설정을 추가로 조정합니다. **Force Mono**를 켜면 스테레오 오디오가 모노로 변환되어 채널 수가 절반이 되므로 메모리도 절반으로 줄어듭니다. 모바일 스피커에서는 스테레오 효과가 미미한 효과음이 많아, 이런 효과음에 적용하면 효과적입니다. **Sample Rate**를 44,100Hz에서 22,050Hz로 낮추면 초당 샘플 수가 절반이 되어 데이터량도 절반으로 줄어듭니다. 짧은 효과음에는 22,050Hz로 충분한 경우가 많습니다. 다만 BGM처럼 품질이 중요한 오디오에는 원본 스테레오와 44,100Hz를 유지합니다.

---

## Import Settings가 빌드 크기와 메모리에 미치는 영향

텍스처, 모델, 오디오의 Import Settings는 빌드 결과물과 런타임 메모리에 직접적인 차이를 만듭니다.
이 중 텍스처는 에셋 유형 중 빌드 크기와 런타임 메모리 비중이 가장 큽니다. 원본 이미지 데이터 자체가 크기 때문에, 같은 해상도라도 압축 포맷 설정 하나로 메모리 사용량이 수 배씩 달라집니다. 일반적인 모바일 게임에서 텍스처가 빌드 크기의 50~70%를 차지하는 경우가 흔하며, Import Settings의 작은 차이 하나가 수십 MB의 빌드 크기 변화로 이어질 수 있습니다.

### 텍스처 압축 포맷 비교

같은 텍스처라도 압축 포맷에 따라 메모리 사용량이 크게 달라집니다. 포맷별 메모리를 비교할 때 기준이 되는 수치는 bpp(bits per pixel), 한 픽셀당 차지하는 비트 수입니다.

<br>

ASTC 포맷의 숫자(4x4, 6x6, 8x8)는 하나의 압축 블록이 커버하는 픽셀 영역을 뜻합니다. 블록 크기와 관계없이 하나의 블록은 항상 128비트(16바이트)로 인코딩되므로, 4x4 블록은 16픽셀을 128비트로, 6x6 블록은 36픽셀을 같은 128비트로 표현합니다. 블록이 클수록 같은 128비트로 더 많은 픽셀을 커버하여 bpp가 낮아지고 용량이 줄지만, 블록 안에서 표현할 수 있는 색상 정보가 제한되어 품질은 떨어집니다.

2048x2048 텍스처 한 장을 기준으로 포맷별 메모리를 비교하면 다음과 같습니다.

**2048 x 2048 텍스처 — 포맷별 메모리 비교**

| 포맷 | bpp | 메모리 (밉맵 제외) | 메모리 (밉맵 포함) |
|---|---|---|---|
| RGBA32 | 32 | 16 MB | 21.3 MB |
| RGBA16 | 16 | 8 MB | 10.6 MB |
| BC7 (PC) | 8 | 4 MB | 5.3 MB |
| ASTC 4x4 | 8 | 4 MB | 5.3 MB |
| ASTC 6x6 | 3.56 | 1.78 MB | 2.37 MB |
| ASTC 8x8 | 2 | 1 MB | 1.33 MB |
| ETC2 (RGB / RGBA) | 4 / 8 | 2 / 4 MB | 2.7 / 5.3 MB |

ETC2는 알파 채널 유무에 따라 bpp가 달라집니다. RGB만 사용하면 4bpp, 알파 채널을 포함하면 8bpp입니다. RGBA32 대비 ASTC 6x6는 약 1/9 크기이며, 어떤 포맷이든 밉맵을 켜면 메모리가 약 33% 추가됩니다.

<br>

2048x2048 텍스처 100장이 있는 프로젝트에서 모두 RGBA32를 사용하면 밉맵 제외 기준으로 약 1.6GB가 필요하지만, ASTC 6x6으로 변환하면 약 178MB로 줄어듭니다. 모바일 기기에서 이 차이는 앱이 정상 실행되느냐, OOM(Out Of Memory)으로 강제 종료되느냐를 가를 수 있습니다.

### Max Size와 밉맵 유무의 영향

2048x2048 ASTC 6x6 텍스처 한 장을 기준으로, Max Size와 밉맵 설정에 따른 메모리 변화입니다.

<br>

**Max Size와 밉맵 조합별 메모리** (ASTC 6x6 기준)

| Max Size | 밉맵 OFF | 밉맵 ON |
|---|---|---|
| 2048 | 1.78 MB | 2.37 MB |
| 1024 | 0.44 MB | 0.59 MB |
| 512 | 0.11 MB | 0.15 MB |
| 256 | 0.03 MB | 0.04 MB |

Max Size를 2048에서 1024로 낮추면 해상도가 가로·세로 각각 절반이 되어 픽셀 수가 1/4로 줄고, 메모리가 약 75% 감소합니다.

<br>

텍스처 최적화에서 가장 효과적인 두 가지 수단은 **압축 포맷**과 **Max Size**입니다. 밉맵은 메모리를 약 33% 더 소비하지만, 3D 오브젝트처럼 카메라 거리에 따라 크기가 변하는 텍스처에서 밉맵을 끄면 오히려 계단 현상(앨리어싱)이 발생합니다.
반면, UI처럼 화면 고정 크기로 표시되는 텍스처는 밉맵이 불필요하므로 끄는 것이 맞습니다. 프로젝트의 텍스처 목록을 메모리 소비 순으로 정렬하고, 상위 항목부터 포맷과 Max Size를 점검하면 적은 작업으로 큰 절약 효과를 얻습니다.

---

## AssetPostprocessor

앞에서 본 Import Settings의 효과를 알고 있어도, 에셋마다 수동으로 설정하면 번거롭고 실수가 발생하기 쉽습니다. 팀 프로젝트에서는 팀원마다 설정이 달라지는 문제도 생깁니다. Unity는 이 문제를 해결하기 위해 **AssetPostprocessor**를 제공합니다.

AssetPostprocessor는 에셋이 임포트될 때 자동으로 실행되는 콜백을 정의하는 클래스입니다.
`OnPreprocessTexture`, `OnPreprocessModel`, `OnPreprocessAudio` 같은 메서드를 오버라이드하면, 임포트 직전에 설정을 코드로 강제할 수 있습니다. 임포트 엔진이 변환을 마친 뒤에는 `OnPostprocessTexture`, `OnPostprocessModel` 등의 후처리 콜백도 호출되므로, 변환 결과를 검증하거나 추가 가공하는 것도 가능합니다.

<br>

<div style="text-align: center;">
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

다음은 팀 단위로 임포트 규칙을 강제하는 예시입니다. 특정 폴더에 있는 텍스처에 자동으로 Max Size와 압축 포맷을 적용합니다.

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

이 스크립트는 `Editor` 폴더에 넣어야 합니다. AssetPostprocessor는 에디터 전용 기능이므로, Editor 폴더 바깥에 두면 빌드에 포함되어 컴파일 오류가 발생합니다.
Editor 폴더에 넣으면 해당 폴더에 텍스처를 추가하거나 재임포트할 때마다 자동으로 규칙이 적용되며, 아티스트가 Import Settings를 직접 건드리지 않아도 폴더 구조에 따라 일관된 설정이 보장됩니다.

<br>

AssetPostprocessor는 텍스처뿐 아니라 모델, 오디오 등 모든 에셋 유형에 대해 콜백을 제공합니다. 모델에 대해 Read/Write Enabled를 강제로 끄거나, 오디오에 대해 Load Type을 자동 설정하는 것도 가능합니다.
여러 AssetPostprocessor 스크립트가 존재할 때는 `GetPostprocessOrder()` 메서드를 오버라이드하여 실행 순서를 제어할 수 있습니다.

---

## 마무리

- Asset Import Pipeline은 소스 에셋을 엔진 내부 포맷으로 변환하며, Import Settings가 빌드 크기와 런타임 메모리를 결정합니다.
- Library 폴더는 재생성 가능하므로 버전 관리에서 제외하고, `.meta` 파일은 GUID를 보관하므로 반드시 포함해야 합니다. `.meta` 파일 삭제 시 GUID가 바뀌어 모든 참조가 깨집니다.
- 텍스처에서는 압축 포맷과 Max Size가 메모리에 가장 큰 영향을 미치며, Read/Write Enabled는 메모리를 2배로 만듭니다.
- 모델에서는 Mesh Compression이 런타임 메모리에 효과가 없다는 점, Optimize Mesh를 항상 켜야 한다는 점을 점검합니다. Animation Type은 용도에 맞게 Generic 또는 Humanoid를 선택합니다.
- 오디오는 Load Type에 따라 메모리-CPU 트레이드오프가 발생합니다. 짧은 효과음은 Decompress On Load, 중간 음성은 Compressed In Memory, BGM은 Streaming이 기본 기준입니다.
- AssetPostprocessor를 활용하면 Import Settings를 코드로 강제하여, 팀 단위의 일관된 설정을 자동으로 보장할 수 있습니다.

에셋 임포트의 모든 설정은 빌드 크기, 메모리 사용량, 품질 사이의 균형점을 결정합니다. 팀 규모가 커질수록 이 균형점을 수동으로 유지하기 어려우므로, AssetPostprocessor를 통한 자동화의 가치도 커집니다.

<br>

이 글에서는 소스 에셋이 임포트 에셋으로 변환되는 과정과, Import Settings가 빌드 크기와 메모리에 미치는 영향을 살펴봤습니다. 임포트된 에셋은 디스크에 직렬화(Serialization)되어 저장되고, 런타임에 역직렬화되어 메모리에 올라갑니다. 이 직렬화-역직렬화 과정은 에셋의 로딩 속도와 메모리 배치에 직접 영향을 줍니다.

[Part 2](/dev/unity/UnityAsset-2/)에서는 Unity의 직렬화 시스템과 Instantiate의 내부 동작을 살펴봅니다. 에셋 메모리의 실질적인 관리 방법은 [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 확인할 수 있습니다.

<br>

---

**관련 글**
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)

**시리즈**
- **Unity 에셋 시스템 (1) - Asset Import Pipeline (현재 글)**
- [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)
- [Unity 에셋 시스템 (3) - Scene Management](/dev/unity/UnityAsset-3/)

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
- **Unity 에셋 시스템 (1) - Asset Import Pipeline** (현재 글)
- [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)
- [Unity 에셋 시스템 (3) - Scene Management](/dev/unity/UnityAsset-3/)
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
