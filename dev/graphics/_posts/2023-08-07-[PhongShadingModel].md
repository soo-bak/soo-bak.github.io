---
layout: single
title: "Phong Shading - soo:bak"
date: "2023-08-07 00:33:00 +0900"
description: "Phong Shading 광원 모델의 개념과 Unity에서의 구현 방법을 설명합니다. Ambient, Diffuse, Specular 반사를 통한 입체감 표현 기법입니다."
pin: true
tags:
  - 그래픽스
  - 셰이딩
  - Phong Shading
  - 광원 모델
  - Unity
  - C#
keywords: "Phong Shading, 퐁 셰이딩, 광원 모델, Ambient, Diffuse, Specular, Unity, 컴퓨터 그래픽스, 셰이더"
---
<br>

## 개념
`Phong Shading`, 퐁 셰이딩은 컴퓨터 그래픽스에서 사용되는 광원 모델의 한 종류로,<br>
<br>
1970년대 초 `Bui Tuong Phong` 에 의해 개발되었다.<br>
<br>
퐁 모델에서는 표면의 반사, 확산, 주변 광에 대하여 시뮬레이션하여 물체에 입체감을 부여한다. <br>
<br><br>

### Ambient Reflection, 주변 반사
<br>
주변 반사는 물체가 받는 주변 환경 광을 나타낸다.<br>
<br>
모든 물체는 주변 환경의 광을 일정량 반사하게 되므로, 이를 통해 실제 세계에서 볼 수 있는 최소한의 밝기를 표현할 수 있다.<br>
<br>
퐁 모델에서의 주변 반사는 다음과 같이 계산된다.<br>
<br>
<b>I<sub>a</sub></b> = <b>I<sub>ambient</sub></b> * <b>K<sub>a</sub></b> <br>
<br>
여기서,<br>
- <b>I<sub>a</sub></b> 는 `최종 주변 반사량`<br>
- <b>I<sub>ambient</sub></b> 는 `주변 광의 강도`<br>
- <b>K<sub>a</sub></b> 는 `물체의 주변 반사 계수`<br>
<br><br>

### Diffuse Reflection, 확산 반사(난반사)
확산 반사는 물체의 불규칙한 표면 때문에 광원의 빛이 여러 방향으로 퍼지는 것을 나타낸다.<br>
<br>
이 반사는 광원의 방향과 물체의 표면 방향에만 의존한다.
<br>
퐁 모델에서의 확산 반사는 다음과 같이 계산된다.<br>
<br>
<b>I<sub>d</sub></b> = <b>I<sub>diffuse</sub></b> * <b>K<sub>d</sub></b> * (<b>N</b> ⋅ <b>L</b>) <br>
<br>
여기서,<br>
- <b>I<sub>d</sub></b> 는 `최종 확산 반사량`<br>
- <b>I<sub>diffuse</sub></b> 는 `광원의 확산 광 강도`<br>
- <b>K<sub>d</sub></b>는 `물체의 확산 반사 계수`<br>
- <b>N</b> 은 `표면의 단위 법선 벡터`<br>
- <b>L</b> 은 `광원의 방향 단위 벡터`<br>
<br>

(<b>N</b> ⋅ <b>L</b>) 로 두 벡터를 내적하기 때문에, 표면과 광원 사이의 각도에 따라서 확산 반사량이 결정된다. <br>
<br><br>

### Specular Reflection, 완전 반사(정반사)
완전 반사는 광원의 빛이 특정 방향으로 집중되어 반사되는 것을 나타낸다.<br>
<br>
물체의 표면의 매끄러움, 광택 등을 표현할 수 있다. <br>
<br>
퐁 모델에서의 완전 반사는 다음과 같이 계산된다. <br>
<br>
<b>I<sub>s</sub></b> = <b>I<sub>specular</sub></b> * <b>K<sub>s</sub></b> * (<b>R</b> ⋅ <b>V</b>)<b><sup>n</sup></b> <br>
<br>
여기서,<br>
- <b>I<sub>s</sub></b> 는 `최종 완전 반사량`<br>
- <b>I<sub>specular</sub></b> 는 `광원의 반사 광 강도`<br>
- <b>K<sub>s</sub></b> 는 `물체의 완전 반사 계수` <br>
- <b>R</b> 은 `반사된 빛의 방향 단위 벡터`<br>
- <b>V</b> 는 `관찰자의 방향 단위 벡터`
- <b>n</b> 은 `반사의 세기 지수`<br>
<br><br>

<br>
최종적으로, 물체의 특정 픽셀에서의 광 반사량은 다음과 같이 계산된다. <br>
<br>
<b>I</b> = <b>I<sub>a</sub></b> + <b>I<sub>d</sub></b> + <b>I<sub>s</sub></b> <br>
<br><br><br>

## 구현 예시 (Unity)


  <p align="center">
    <img src="/assets/images/slide_res/PhongShading.gif" align="center" width="55%">
    <figcaption align="center">Phong Shading</figcaption>
  </p>

<br><br><br>

  ```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PhongShadingModel : MonoBehaviour
{
  public Light lightSource;

  public Color objectColor = Color.white;

  [Range(0, 1)]
  public float ambientIntensity = 1f;

  [Range(0, 1)]
  public float diffuseIntensity = 0f;

  [Range(0, 1)]
  public float specularIntensity = 0f;

  public float shininess = 10f;

  public Slider redSlider, greenSlider, blueSlider;

  public Slider ambientSlider, diffuseSlider, specularSlider;

  private Mesh mesh;

  private Vector3[] normals;

  private Color[] colors;

  private void Start() {
    mesh = GetComponent<MeshFilter>().mesh;
    normals = mesh.normals;
    colors = new Color[normals.Length];

    ambientSlider.onValueChanged.AddListener(UpdateAmbientIntensity);
    diffuseSlider.onValueChanged.AddListener(UpdateDiffuseIntensity);
    specularSlider.onValueChanged.AddListener(UpdateSpecularIntensity);
    redSlider.onValueChanged.AddListener(UpdateRedColor);
    greenSlider.onValueChanged.AddListener(UpdateGreenColor);
    blueSlider.onValueChanged.AddListener(UpdateBlueColor);

    ambientSlider.value = ambientIntensity;
    diffuseSlider.value = diffuseIntensity;
    specularSlider.value = specularIntensity;
    redSlider.value = objectColor.r;
    greenSlider.value = objectColor.g;
    blueSlider.value = objectColor.b;
  }

  private void Update() {
    CalculatePhongShading();
    mesh.colors = colors;
  }

  private void CalculatePhongShading() {
    for (int i = 0; i < normals.Length; i++) {
      Vector3 worldNormal = transform.TransformDirection(normals[i]);
      Vector3 toLight = (lightSource.transform.position - transform.position).normalized;
      Vector3 toCamera = (Camera.main.transform.position - transform.position).normalized;
      Vector3 reflected = Vector3.Reflect(-toLight, worldNormal);

      // Ambient
      Color ambient = objectColor * ambientIntensity;

      // Diffuse
      float diffuseFactor = Mathf.Max(Vector3.Dot(worldNormal, toLight), 0);
      Color diffuse = objectColor * lightSource.color * diffuseFactor * diffuseIntensity;

      // Specular
      float specFactor = Mathf.Pow(Mathf.Max(Vector3.Dot(reflected, toCamera), 0), shininess);
      Color specular = lightSource.color * specFactor * specularIntensity;

      colors[i] = new Color(
        Mathf.Clamp01(ambient.r + diffuse.r + specular.r),
        Mathf.Clamp01(ambient.g + diffuse.g + specular.g),
        Mathf.Clamp01(ambient.b + diffuse.b + specular.b)
      );
    }
  }

  private void UpdateAmbientIntensity(float value) {
    ambientIntensity = value;
  }

  private void UpdateDiffuseIntensity(float value) {
    diffuseIntensity = value;
  }

  private void UpdateSpecularIntensity(float value) {
    specularIntensity = value;
  }

  private void UpdateRedColor(float value) {
    objectColor.r = value;
  }

  private void UpdateGreenColor(float value) {
    objectColor.g = value;
  }

  private void UpdateBlueColor(float value) {
    objectColor.b = value;
  }
}
  ```
<br>
