---
layout: single
title: "[백준 15552] 빠른 A+B (C#, C++) - soo:bak"
date: "2023-05-16 15:20:00 +0900"
---

## 문제 링크
  [15552번 - 빠른 A+B](https://www.acmicpc.net/problem/15552)

## 설명
각 언어별 빠른 입/출력 방법과 관련된 문제입니다. <br>

<br>
<b>[ C# ] </b>
<br>
`C#` 에서의 `string` 자료형은 불변(immutable)입니다. 즉, 한 번 생성된 `string` 객체는 변경할 수 없습니다. <br>
따라서, `string` 자료형에 대한 결합, 삽입, 삭제 등의 조작을 할 때마다 새로운 `string` 객체가 생성되고,<br>
이전의 `string` 객체는 가비지 컬렉션의 대상이 됩니다.<br>
이러한 과정은 메모리의 할당과 해제에 대한 비용이 많이 들고, 특히 크기가 크거나 연산이 많은 경우에 비효율적입니다. <br>
<br>
`StringBuilder` 클래스는 해당 문제를 해결하기 위해 도입되었습니다. <br>
`StringBuilder` 클래스는 내부적으로 문자의 배열을 유지하며, 문자열 조작이 발생하면 해당 배열 내에서 직접적인 변경을 수행합니다. <br>
따라서, 새로운 객체를 계속 새로 생성하거나 메모리를 할당/해제에 관련된 비용을 크게 줄일 수 있습니다. <br>
<br>

<b>[ C++ ] </b>
<br>
`C++` 에서는 `ios::sync_with_stdio(false);` 와 `cin.tie(nullptr);` 을 이용하여 입/출력 속도를 빠르게 할 수 있습니다. <br>

- `ios::sync_with_stdio(false);` : `C++` 의 입출력 라이브러리인 `iostream` 과 `C` 의 입출력 라이브러리 `stdio` 사이의 동기화를 끄는 역할을 합니다. <br>
기본적으로, 이 두 라이브러리는 서로 동기화되어 있어서, 두 라이브러리를 혼합하여 사용할 경우에도 올바른 결과를 얻을 수 있지만, 동기화 작업에는 비교적 많은 시간이 소요됩니다.<br>
따라서, 두 라이브러리를 혼합하여 사용하지 않는다면 해당 동기화를 끄는 것이 입/출력 속도를 향상시킬 수 있습니다.<br>

- `cin.tie(nullptr);` : 기본적으로 `cin` 과 `cout` 은 `tie` 되어있습니다.<br>
즉, `cout` 을 사용하여 출력한 후, `cin` 을 사용하여 입력을 받을 경우, 입력을 받기 전에 출력 버퍼를 자동적으로 비워주게 됩니다.<br>
이 작업 또한 시간이 소요되므로, `tie` 를 끊어내면 입/출력 속도를 향상시킬 수 있습니다.<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  using System.Text;
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      var sb = new StringBuilder();

      for (int i = 0; i < cntCase; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var a = int.Parse(input[0]);
        var b = int.Parse(input[1]);

        sb.AppendLine((a + b).ToString());
      }

      Console.Write(sb);

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase; cin >> cntCase;

  for (int i = 0; i < cntCase; i++) {
    int a, b; cin >> a >> b;
    cout << a + b << "\n";
  }

  return 0;
}
  ```
