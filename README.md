# MasterPC_ws

> 버전: v1 | 최종 수정: 2026-06-10

RoboCup SML 프로젝트의 마스터 PC 워크스페이스입니다.
주어진 오더를 분석하여 실행 계획을 생성하고,
AMR과 워크벤치에 명령을 내리는 시스템입니다.

---

## 📦 패키지 구조

```
MasterPC_ws/src/
  sml_msgs/                  # 공용 메시지 / 서비스 / 액션 패키지
    msg/
      Order.msg
      Station.msg
      Task.msg
      Step.msg
    srv/
      GetPlan.srv
    action/
      NavTask.action          ← 자율주행팀 인터페이스
      WbTask.action           ← Manipulation팀 인터페이스

  sml_system_pkg/            # 시스템 노드 패키지
    sml_system_pkg/
      sml_planning_node.py   # 스텝 시퀀스 생성 노드
      sml_manager_node.py    # 실행 관리 노드
      sml_order_server.py    # 테스트용 Task 발행 노드
```

---

## 🗂️ 노드 역할

| 노드 | 역할 |
|------|------|
| `sml_planning_node` | Task를 받아 depends_on 기반 스텝 시퀀스 생성 |
| `sml_manager_node` | 스텝을 받아 AMR / WB에 병렬 명령 실행 |
| `sml_order_server` | 테스트용 Task 발행 |

---

## 🔗 통신 구조

```
sml_order_server
      ↓ Topic /sml/task
  ┌───┴──────────────────────┐
  ↓                          ↓
sml_planning_node    ────   sml_manager_node
Service /sml/get_plan  ↑ 
                         |
              ┌──────────┼──────────┐
              ↓          ↓          ↓
        amr_nav_node  amr_robot_node  workbench_node
        (자율주행팀)    (Manipulation)  (Manipulation)
```

| 구분 | 방식 | 이름 | 설명 |
|------|------|------|------|
| Task 수신 | Topic | `/sml/task` | planning / manager 둘 다 구독 |
| 스텝 전달 | Service | `/sml/get_plan` | manager 요청 → planning 응답 |
| AMR 이동 | Action | `navigate_to_station` | manager → 자율주행팀 |
| AMR 팔 | Service | `/amr_robot_command` | manager → amr_robot_node |
| 워크벤치 | Action | `wb_task` | manager → Manipulation |
| 상태 모니터링 | Topic | `/sml/status` | manager 발행 |

---

## 📨 인터페이스 정의

### NavTask.action (자율주행팀 전달용)

```
# Goal
int32  station_id       # 이동할 스테이션 번호

---
# Feedback
string status           # "MOVING" / "ARRIVED"

---
# Result
bool   success
string fail_reason      # "NAV_FAILED" / "OBSTACLE" / "TIMEOUT"
```

### WbTask.action (Manipulation 전달용)

```
# Goal
string  work_type       # "PRODUCE" / "RECYCLE"
int32   product_id      # 만들거나 분해할 product_id (예: 13, 81)

---
# Feedback
string status           # "PROCESSING" / "PRODUCING" / "RECYCLING"

---
# Result
bool    success
string  fail_reason
```

### ArmCommand.srv (amr_robot_ws 참고)

```
# Request
string  action          # "LOAD" / "UNLOAD"
int32[] object_ids      # 처리할 물체 ID 리스트

---
# Response
bool    success
int32[] slots
int32[] object_ids
string  message
```

---

## 🚗 AMR 슬롯 구조

| 슬롯 | 용도 |
|------|------|
| 슬롯 1 | 완성품 / 분해 대상 전용 |
| 슬롯 2~6 | 재료 전용 (최대 5개) |

---

## 📋 스텝 구조 (Step.msg)

| 필드 | 타입 | 설명 |
|------|------|------|
| step_id | int32 | 스텝 식별자 |
| type | int32 | AMR=0 / WB=1 |
| action | int32 | LOAD=0 / UNLOAD=1 / PRODUCE=2 / RECYCLE=3 |
| object_ids | int32[] | 재료 또는 완성품 ID |
| station_id | int32 | 실행할 스테이션 ID |
| depends_on | int32[] | 선행 완료되어야 할 step_id 리스트 |

---

## ⚙️

이 워크스페이스는 `amr_robot_ws`의 `arm_interfaces` 패키지를 참조합니다.
**반드시 `amr_robot_ws`를 먼저 빌드하고 source해야 합니다.**

- `amr_robot_ws`: https://github.com/chaerin33/amr_robot_ws

---

## 🔨 빌드 방법

```bash
# 1. amr_robot_ws 먼저 빌드
cd ~/robocup/amr_robot_ws
colcon build
source install/setup.bash

# 2. MasterPC_ws 빌드
cd ~/robocup/MasterPC_ws
colcon build
source install/setup.bash
```

---

## ▶️ 실행 방법

터미널마다 아래 source를 먼저 실행하세요:

```bash
source /opt/ros/humble/setup.bash
source ~/robocup/amr_robot_ws/install/setup.bash
source ~/robocup/MasterPC_ws/install/setup.bash
```

**터미널 1 — planning 노드**
```bash
ros2 run sml_system_pkg sml_planning_node
```

**터미널 2 — manager 노드**
```bash
ros2 run sml_system_pkg sml_manager_node
```

**터미널 3 — 테스트용 Task 발행**
```bash
ros2 run sml_system_pkg sml_order_server
```

**디버깅**
```bash
# 서비스 직접 호출
ros2 service call /sml/get_plan sml_msgs/srv/GetPlan

# 상태 모니터링
ros2 topic echo /sml/status

# 노드 목록 확인
ros2 node list
```

---


## 🔗 연관 저장소

| 저장소 | 담당 | 설명 |
|--------|------|------|
| [MasterPC_ws](https://github.com/chaerin33/MasterPC_ws) | - | 이 저장소 |
| [amr_robot_ws](https://github.com/chaerin33/amr_robot_ws) | Manipulation | AMR 로봇팔 제어 |
| amr_nav_ws | 자율주행팀 | AMR 자율주행 |
| workbench_ws | Manipulation | 워크벤치 제어 |

---
