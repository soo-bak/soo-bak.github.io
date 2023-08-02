---
layout: single
title: "Gaussian Blur - soo:bak"
date: "2023-08-02 15:01:00 +0900"
---
<br>

## 개념
`Gaussian Blur` 는 컴퓨터 그래픽스에서 많이 사용되는 중 블러링 기술 중 하나이다. <br>
<br>
이미지의 픽셀 값을 해당 픽셀 주변의 <b>가중치</b>가 적용된 픽셀 값들의 평균으로 대체함으로 이미지를 블러링한다.<br>
<br>
`Gaussian Blur` 의 이름은 이 블러링 기술에서 사용하는 가중치가 `Gaussian` 함수(정규 분포)를 따르기 때문에 붙여졌으며,<br>
<br>
`Gaussian` 함수는 중심에서 멀어질수록 값이 급격히 줄어드는 특성을 가지고 있다.<br>
<br>
따라서, `Gaussian Blur` 를 적용하면 픽셀 값의 변경은 주로 중심 픽셀과 가까운 이웃 픽셀들에 의해 영향을 받게 되며, <br>
<br>
멀리 떨어진 픽셀들의 영향은 상대적으로 작아진다.<br>

## Box Blur 와의 차이
`Gaussian Blur` 는 `Gaussian 분포` 에 따라 픽셀의 블러 처리를 하기 때문에,<br>
<br>
중심 픽셀에 가까운 픽셀들에게는 높은 가중치를, 중심픽셀로부터 멀리 떨어진 픽셀들에게는 낮은 가중치를 부여하여 픽셀값을 조정한다. <br>
<br>
이 방식은 블러 처리가 자연스러워 보이도록 만들어주며, 보다 세밀한 처리를 가능하게 한다.<br>
<br>
<br>
반면에, `Box Blur` 는 각 픽셀에 동일한 가중치를 부여하여 블러 처리를 진행한다.<br>
<br>
즉, 주어진 범위 내의 모든 픽셀 값들을 동일하게 처리하여 그 평균 값을 취하는 방식이다. <br>
<br>
이 방식은 연산이 간단하여 빠른 처리 속도를 가지지만, `Gaussian Blur` 에 비해 자연스러운 블러 효과를 얻기 어렵다.<br>
<br><br>
- `Box Blur` 와 `Gaussian Blur` 의 차이 비교<br>

    <p align="center">
    <img src="/assets/images/slide_res/BoxBlur_00.gif" align="left" width="45%">
    <img src="/assets/images/slide_res/GaussianBlur_00.gif" align="right" width="45%">
    <figcaption align="center">Box Blur(왼쪽), Gaussian Blur(오른쪽)</figcaption>
  </p>
<br>

## 구현 방법
먼저, `Gaussian Kernel` 을 생성한다. `Kernel` 은 보통 정사각형 행렬로 표현되며, 각 셀의 값은 중심 셀에 대한 거리에 따라 `Gaussian` 함수를 사용해 계산된다.<br>
<br>
`Kernel` 의 크기는 보통 홀수인데, 이는 중심 셀을 가질 수 있기 때문이다. <br>
<br>
행렬의 각 값은 `Gaussian` 분포를 따르며, 중심이 되는 픽셀에 최대 가중치를 주고 멀어질수록 가중치를 감소시킨다. <br>
<br><br>
`Gaussian Kernel` 을 생성한 후, 이 `Kernel` 을 이미지에 적용한다. <br>
<br>
이 과정에서 `Kernel` 의 각 셀과 이미지의 해당 픽셀이 곱해진 값들을 모두 합하고, 그 결과를 원래 픽셀 위치의 값으로 설정하며,<br>
<br>
위 과정을 모든 픽셀에 대하여 반복한다.<br>
<br><br>
위의 `Convolution` 결과, 픽셀 값이 그 범위를 초과할 수도 있기 때문에 마지막으로 모든 픽셀 값을 정규화하여 `0` 과 `255` 사이의 값으로 만들어야 하는데, 이는 색상 값이 일반적으로 `8` 비트 정수로 표현되기 때문이다.<br>
<br>
<br>
위의 과정은 각 색상 채널에 대해 별도로 적용되어야 하며, 컬러 이미지의 경우 일반적으로 각각의 레드, 그린, 블루 채널에 대해 `Gaussian Blur` 를 적용한다.<br>
<br>

## 예시
- `Gaussian Blur`
    <p align="center">
    <img src="/assets/images/slide_res/GaussianBlur_00.gif" align="center" width="70%">
    <figcaption align="center">가로 방향으로만 적용</figcaption>
  </p>
<br>
