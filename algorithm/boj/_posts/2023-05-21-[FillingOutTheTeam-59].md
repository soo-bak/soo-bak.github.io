---
layout: single
title: "[백준 4758] Filling Out the Team (C#, C++) - soo:bak"
date: "2023-05-21 07:52:00 +0900"
---

## 문제 링크
  [4758번 - Filling Out the Team](https://www.acmicpc.net/problem/4758)

## 설명
입력으로 주어지는 선수들의 능력치(속도, 체중, 힘)를 바탕으로,<br>

선수가 어떤 포지션에 적합한지를 판단하는 문제입니다. <br>

선수가 특정 포지션에 적합하려면 그 포지션의 최소 체중과 힘을 만족해야 하며, 동시에 최대 속도 이하를 유지해야 합니다. <br>

입력으로 주어지는 선수의 능력치들이 각 포지션의 요구사항을 만족하는지 검사하여, 만족하는 포지션이 있다면 그 이름을 출력합니다. <br>

만족하는 포지션이 없다면 "No positions" 을 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    class Position {
      public string Name { get; }
      public double MinSpeed { get;}
      public int MinWeight { get; }
      public int MinStrength { get; }
      public Position(string name, double minSpeed, int minWeight, int minStrength) {
        Name = name;
        MinSpeed = minSpeed;
        MinWeight = minWeight;
        MinStrength = minStrength;
      }
    };

    static void Main(string[] args) {

      var positions = new List<Position> {
        new Position("Wide Receiver", 4.5, 150, 200),
        new Position("Lineman", 6.0, 300, 500),
        new Position("Quarterback", 5.0, 200, 300)
      };

      while (true) {
        var input = Console.ReadLine()!.Split(' ');
        var speed = double.Parse(input[0]);
        var weight = int.Parse(input[1]);
        var strength = int.Parse(input[2]);

        if (speed == 0 && weight == 0 && strength == 0) break ;

        var playable = new List<string>();
        foreach (var position in positions) {
          if (speed <= position.MinSpeed && weight >= position.MinWeight &&
              strength >= position.MinStrength)
            playable.Add(position.Name);
        }

        if (playable.Count == 0) Console.WriteLine("No positions");
        else Console.WriteLine(string.Join(" ", playable));
      }

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

struct Position {
  string name;
  double minSpeed;
  int minWeight;
  int minStrength;
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<Position> positions {
    {"Wide Receiver", 4.5, 150, 200},
    {"Lineman", 6.0, 300, 500},
    {"Quarterback", 5.0, 200, 300}
  };

  while (true) {
    double speed;
    int weight, strength;
    cin >> speed >> weight >> strength;

    if (speed == 0 && weight == 0 && strength == 0) break ;

    vector<string> playable;
    for (const auto& posiiton : positions) {
      if (speed <= posiiton.minSpeed && weight >= posiiton.minWeight &&
          strength >= posiiton.minStrength)
        playable.push_back(posiiton.name);
    }

    if (playable.empty()) cout << "No positions\n";
    else {
      for (const auto& position : playable)
        cout << position << " ";
      cout << "\n";
    }
  }

  return 0;
}
  ```
