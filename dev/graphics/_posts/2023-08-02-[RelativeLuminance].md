---
layout: single
title: "Relative Luminance - soo:bak"
date: "2023-08-02 15:55:00 +0900"
description: "Relative Luminance(상대적 루미넌스) 개념과 계산 방법을 설명합니다. RGB 색상의 밝기를 인간의 눈 감도에 맞게 계산하는 방법입니다."
tags:
  - 그래픽스
  - 색상
  - Luminance
  - RGB
  - 컴퓨터 그래픽스
keywords: "Relative Luminance, 상대적 루미넌스, 밝기, RGB, 색상 처리, 이미지 처리, 컴퓨터 그래픽스"
---
<br>

## 개념
`Relative Luminance`, 상대적 루미넌스는 빛의 밝기를 나타내는 측정값인 `Luminance` 를 표준화한 형태로 표현한 것이다. <br>
<br>
`Relative Luminance` 는 색상의 RGB 성분을 기반으로 계산된다. <br>
<br>
색상이 인간의 눈에 어떻게 보이는지는 RGB 성분 각각에 대한 인간의 감도에 따라 달라지는데, <br>
<br>
인간의 눈은 특히 녹색에 가장 민감하며, 빨강에는 중간 정도의 민감도를 가지고, 파랑에는 가장 덜 민감하다고 한다.<br>
<br>
<br>
따라서, 각 색상별 가중치를 다르게 적용하여 `Relatve Luminance` 는 다음과 같이 계산된다.<br>
<br><br>

`Y` = `0.2126` * `R` + `0.7152` * `G` + `0.0722` * `B`
<br><br><br>

여기서, `Y` 는 `Relative Luminance` 이며, `R`, `G`, `B` 는 각각 빨강, 녹색, 파랑 색상 성분의 비율이다. <br>
<br>
각각의 계수들은 인간의 눈의 색상 감도를 반영한 가중치이다. <br>
<br>
<br>
`Relative Luminance` 는 그래픽스 및 이미지 처리에서 많은 용도로 사용되는데, <br>
<br>
예를 들어, 이미지의 명암 대비를 조절하거나, 색상 이미지를 흑백으로 변환하거나, 특정 색상이 인간의 눈에 얼마나 밝게 보일지를 예측하는 데에 사용된다.<br>
<br>
