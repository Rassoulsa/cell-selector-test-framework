# Embedded Device Test Automation Framework  
### Robotic Cell-Selection System Validation

## 📌 Overview
This project implements an automated test framework for validating an embedded robotic imaging system used in cell-selection devices.  
It focuses on structured software testing, hardware abstraction, and automated validation of device workflows.

The framework simulates real-world testing of embedded medical devices by combining:
- Device communication
- Hardware control abstraction
- Automated test execution
- Structured reporting

---

## 🎯 Objectives
- Develop automated test workflows for embedded systems  
- Validate hardware-software integration  
- Implement component, functional, integration, and end-to-end tests  
- Provide structured test reporting and logging  
- Simulate realistic device behavior without physical hardware  

---

## 🏗️ Architecture

Communication Layer
├─ Serial Client
├─ Protocol Parser
└─ Connection Manager

Device Abstraction Layer
├─ Motor Controller
├─ Robot Arm
├─ Camera Module
└─ Device Status

Test Framework Core
├─ Test Runner
├─ Report Generator
├─ Logger
└─ Custom Exceptions

Test Suites
├─ Component Tests
├─ Functional Tests
├─ Integration Tests
└─ End-to-End Tests
## 🧪 Test Levels

### Component Tests
Validation of individual subsystems:
- Motor control
- Serial communication
- Camera module

### Functional Tests
Behavior verification:
- Motion accuracy
- Timeout handling
- Error management

### Integration Tests
Interface validation between modules:
- Vision → Motion pipeline
- Inter-module communication

### End-to-End Tests
Full system workflow simulation:
- System startup
- Device health check
- Image capture
- Target detection
- Motion execution
- Robotic interaction

---

## ⚙️ Technologies Used
- Python 3.x  
- pytest  
- pyserial  
- Logging framework  
- Dataclasses  

---

## 📊 Reporting
The framework generates structured test reports including:
- Execution summary
- Pass / Fail statistics
- Error tracking
- Duration metrics

Reports are exported in JSON format for CI/CD and dashboard integration.

---

## 🚀 How to Run Tests

### Run all tests
```bash
pytest -v


Run specific test category
pytest -m smoke
pytest -m regression
pytest -m integration
pytest -m e2e

Project Structure
cell-selector-test-framework/
├── docs/
├── src/
├── testsuites/
├── pytest.ini
├── requirements.txt
└── README.md