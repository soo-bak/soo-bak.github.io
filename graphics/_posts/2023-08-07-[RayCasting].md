---
layout: single
title: "Ray Casting - soo:bak"
date: "2023-08-07 08:59:00 +0900"
---
<br>

## 개념
`Ray Casting` 은 가상의 카메라에서 특정 방향으로 '레이, (빛)' 또는 '선' 을 발사하여,<br>
<br>
그 레이가 어떤 물체와 만나는지를 계산하여 다양한 시각적 처리를 할 수 있는 기법이다. <br>
<br>
레이는 기본적으로 시작점과 방향으로 정의가 되는데, 둘 모두 벡터를 통해 계산하며, 레이를 수학적으로 표현하면 다음과 같다.<br>
<br>
Ray(t) = Origin + t * Direction <br>
<br>
여기서,<br>
  - Origin 은 레이의 시작점<br>
  - Direction 은 레이의 방향<br>
  - t 는 레이가 얼마나 "멀리" 확장될지에 대한 스칼라값 <br>

## 활용 사례
`Ray Casting` 은 다양하게 활용할 수 있다.<br>
<br>
특히 현대 게임에서는 물체 간의 충돌 감지, 시야 판별, 그림자 및 반사 효과 구현,<br>
<br>
사용자의 입력이 물체와 접촉했는지에 대한 판별, FPS 게임에서 총알의 피격 여부 등등<br>
<br>
정말 다양한 방법으로 활용이 가능한 기법이다. <br>
<br>
모든 활용은 위의 기본적인 레이의 수식으로부터 시작된다. <br>
<br>
예를 들어, 레이를 통해 가상의 구를 그리거나, 구와와의 상호작용 여부 등을 판별하려면 다음과 같이 수식을 풀어나간다. <br>
<br>
(P - C) ⋅ (P - C) = r<sup>2</sup> <br>
<br>
여기서,<br>
  - P 는 레이 위의 임의의 점
  - C 는 구의 중심
  - r 은 구의 반지름
<br>

으로 표현했을 때, 레이 위의 어떤 점 P 가 구와 부딪혔는지, 혹은 구의 밖에 있는지, 아니면 구의 안에 있는지 등등을 다음과 같이 계산할 수 있다.<br>
<br>
(Origin + t * Direction - C) ⋅ (Origin + t * Direction - C) = r<sup>2</sup> <br>
<br>
이 때, (Origin + t * Direction - C) 벡터를 Diff(t) = Origin + t * DIrection - C 라 하면, <br>
<br>
내적의 정의에 따라 Diff(t) ⋅ Diff(t) = |Diff(t)|<sup>2</sup> 이 되므로, <br>
<br>
(Direction ⋅ Direction) * t<sup>2</sup> + 2 * (Direction ⋅ (Origin - C)) * t + (Origin - C) ⋅ (Origin - C) 가 되며, <br>
<br>
이를 t 에 대한 2차 방정식<br>
<br>
at<sup>2</sup> + bt + c = 0 으로 간단하게 표현할 수 있다.
<br>
여기서,<br>
  - a = Direction ⋅ Direction <br>
  - b = 2(Direction ⋅ (Origin - C)) <br>
  - c = (Origin - C) ⋅ (Origin - C) - r<sup>2</sup> <br>
<br>

따라서, 레이의 길이 t 에 따라서 구를 활용한 다양한 처리들을 할 수 있게 된다. <br>
<br>
구 이외에도 하나의 레이만으로도 다양한 처리들을 할 수 있으며, 활용 사례는 무궁무진하다. <br>
<br>
Unity 게임 엔진에서는 API 를 통해 직접 자료형을 제공해주며, 쉽게 사용이 가능하도록 되어있다. <br>
<br>

## 예시 (Unity)

  <p align="center">
    <img src="/assets/images/slide_res/RayCastingExample.gif" align="center" width="75%">
    <figcaption align="center">직접 Ray 를 그려보면 직관적으로 이해할 수 있다</figcaption>
  </p>

<br><br><br>

[ 코드 ]<br>
  ```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;

public class RayCastingFOV : MonoBehaviour {

  public int numberOfRays = 720;

  public float fov = 60f;

  public float rayDistance = 1f;

  public LayerMask wallMask;

  public Color visibleColor = Color.yellow;

  public Color nonVisibleColor = Color.black;

  private void Update() {
    foreach (Transform child in transform) {
      Destroy(child.gameObject);
    }

    for (int i = 0; i < numberOfRays; i++) {
      float angle = (i / (float)numberOfRays) * 360 - 180;
      Vector3 rayDirection = Quaternion.Euler(0, angle, 0) * transform.forward;

      Ray ray = new Ray(transform.position, rayDirection);
      RaycastHit hit;

      Color rayColor = nonVisibleColor;

      if (angle >= -fov / 2 && angle <= fov / 2)
        rayColor = visibleColor;

      LineRenderer line = CreateLineRenderer(rayColor);
      line.SetPosition(0, transform.position);

      if (Physics.Raycast(ray, out hit, rayDistance, wallMask))
        line.SetPosition(1, hit.point);
      else
        line.SetPosition(1, transform.position + rayDirection * rayDistance);
    }
  }
  private LineRenderer CreateLineRenderer(Color color) {
    GameObject lineObject = new GameObject("Line");
    lineObject.transform.SetParent(transform);
    LineRenderer line = lineObject.AddComponent<LineRenderer>();
    line.material = new Material(Shader.Find("UI/Default"));
    line.startColor = color;
    line.endColor = color;
    line.startWidth = 0.01f;
    line.endWidth = 0.1f;
    line.positionCount = 2;
    return line;
  }
}
  ```
<br><br><br>
추가 - C언어와 Ray Casting 을 활용한 DOOM 모작 프로젝트 - soo:bak<br>
  <p align="center">
    <img src="/assets/images/slide_res/RayCastingExample2.gif" align="center" width="55%">
    <figcaption align="center">DOOM 모작</figcaption>
  </p>
<br>
