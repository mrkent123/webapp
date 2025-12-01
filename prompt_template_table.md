# BẢNG PROMPT TEMPLATE - iPhone Clone to PWA

## 🔧 EXECUTION AGENT PROMPTS

| **PROMPT TIẾNG ANH** | **GIẢI THÍCH TIẾNG VIỆT** |
|----------------------|-----------------------------|
| **Setup Phase** | |
| `Install and configure libimobiledevice toolkit on Linux system for iOS device communication` | Cài đặt libimobiledevice để Linux có thể giao tiếp với iPhone |
| `Verify iPhone connection via USB and establish secure pairing` | Kiểm tra kết nối iPhone và tạo pairing an toàn |
| `Mount iPhone filesystem and list all installed applications` | Mount file system iPhone và lấy danh sách apps |
| | |
| **App Selection & Extraction** | |
| `Extract IPA file from target iPhone application for static analysis` | Trích xuất file IPA từ app target để phân tích tĩnh |
| `Perform static analysis of IPA contents including Info.plist, resources, and binary structure` | Phân tích tĩnh nội dung IPA (Info.plist, resources, binary) |
| `Identify and catalog all UI components, assets, and API endpoints used by the application` | Xác định và catalog UI components, assets, API endpoints |
| | |
| **Dynamic Analysis** | |
| `Setup Frida and Objection for dynamic analysis of iOS application runtime behavior` | Setup Frida + Objection để phân tích runtime behavior |
| `Monitor application API calls, network requests, and data flows` | Monitor API calls, network requests, data flows của app |
| `Capture screenshots and create UI/UX flow mapping` | Chụp screenshots và tạo UI/UX flow mapping |
| `Document application architecture and business logic` | Document architecture và business logic của app |
| | |
| **UI Cloning** | |
| `Recreate application UI components using HTML5, CSS3, and JavaScript` | Tái tạo UI components bằng HTML5, CSS3, JS |
| `Implement responsive design for mobile, tablet, and desktop viewports` | Implement responsive design cho mobile/tablet/desktop |
| `Recreate animations, transitions, and interactive elements` | Tái tạo animations, transitions, interactive elements |
| `Optimize assets (images, fonts, styles) for web delivery` | Optimize assets cho web delivery |
| | |
| **Business Logic Implementation** | |
| `Implement core application business logic and algorithms` | Implement business logic và algorithms cốt lõi |
| `Setup API integration endpoints for data fetching and authentication` | Setup API integration cho data fetching và authentication |
| `Implement local storage and offline capabilities` | Implement local storage và offline capabilities |
| `Handle user authentication and session management` | Handle authentication và session management |
| | |
| **PWA Conversion** | |
| `Create Web App Manifest with all required properties and icons` | Tạo Web App Manifest với properties và icons cần thiết |
| `Implement Service Worker for offline functionality and caching` | Implement Service Worker cho offline và caching |
| `Setup PWA installability features and browser compatibility` | Setup PWA installability và browser compatibility |
| `Optimize PWA performance and accessibility` | Optimize PWA performance và accessibility |
| | |
| **Testing & Validation** | |
| `Perform comprehensive testing across mobile, tablet, and desktop browsers` | Test comprehensive trên mobile/tablet/desktop browsers |
| `Validate PWA compliance using Lighthouse audit` | Validate PWA compliance bằng Lighthouse audit |
| `Compare clone functionality with original iPhone application` | So sánh functionality của clone với app iPhone gốc |
| `Generate performance report and optimization recommendations` | Tạo performance report và optimization recommendations |
| | |
| **Deployment** | |
| `Package PWA for production deployment` | Package PWA cho production deployment |
| `Deploy to web server with proper configuration` | Deploy lên web server với configuration phù hợp |
| `Setup CDN and performance optimization` | Setup CDN và performance optimization |
| `Generate deployment documentation and maintenance guide` | Tạo deployment documentation và maintenance guide |

---

## 🎯 EXECUTION WORKFLOW COMMANDS

| **HIGH-LEVEL COMMAND** | **MỤC ĐÍCH CHI TIẾT** |
|------------------------|-------------------------|
| `Execute complete iPhone app to PWA conversion workflow` | Chạy toàn bộ workflow clone iPhone app thành PWA |
| `Install and configure all required development tools and dependencies` | Cài đặt và configure tất cả tools và dependencies cần thiết |
| `Perform comprehensive analysis of target iPhone application` | Thực hiện phân tích toàn diện target iPhone app |
| `Create pixel-perfect clone with full functionality replication` | Tạo clone pixel-perfect với full functionality replication |
| `Convert web app to PWA with offline capabilities` | Convert web app thành PWA với offline capabilities |
| `Deploy and validate production-ready PWA` | Deploy và validate PWA ready cho production |

---

## 🔍 ANALYSIS & MONITORING PROMPTS

| **MONITORING COMMAND** | **GIẢI THÍCH** |
|------------------------|----------------|
| `Monitor system resources and performance during analysis` | Monitor system resources và performance trong quá trình phân tích |
| `Validate each phase completion before proceeding to next step` | Validate hoàn thành mỗi phase trước khi proceed step tiếp theo |
| `Generate detailed logs and progress reports` | Tạo detailed logs và progress reports |
| `Handle errors gracefully with fallback options` | Handle errors gracefully với fallback options |
| `Ensure data integrity throughout the conversion process` | Đảm bảo data integrity trong suốt conversion process |

---

## ⚡ QUICK EXECUTION COMMANDS

| **SHORT COMMAND** | **FULL EXPLANATION** |
|-------------------|---------------------|
| `Start iPhone connection setup` | Bắt đầu setup kết nối iPhone |
| `Extract target application data` | Trích xuất target application data |
| `Analyze app structure and UI` | Phân tích app structure và UI |
| `Clone interface and functionality` | Clone interface và functionality |
| `Convert to PWA format` | Convert thành PWA format |
| `Deploy and test final result` | Deploy và test kết quả cuối cùng |

---

## 🎮 INTERACTIVE DEBUGGING COMMANDS

| **DEBUG COMMAND** | **PURPOSE** |
|-------------------|-------------|
| `Enable verbose logging for troubleshooting` | Enable verbose logging để troubleshoot |
| `Stop and resume execution at specific checkpoints` | Stop và resume execution tại specific checkpoints |
| `Generate diagnostic reports for complex issues` | Generate diagnostic reports cho complex issues |
| `Rollback to previous working state if needed` | Rollback về previous working state nếu cần |
| `Invoke manual intervention for approval or decisions` | Invoke manual intervention cho approval hoặc decisions |

---

## 📊 QUALITY ASSURANCE PROMPTS

| **QA COMMAND** | **QUALITY CHECK** |
|----------------|------------------|
| `Validate visual accuracy against original app screenshots` | Validate visual accuracy với original app screenshots |
| `Test all interactive elements and user workflows` | Test tất cả interactive elements và user workflows |
| `Verify PWA compliance and performance metrics` | Verify PWA compliance và performance metrics |
| `Cross-browser and cross-device compatibility testing` | Cross-browser và cross-device compatibility testing |
| `Final user acceptance testing and documentation` | Final user acceptance testing và documentation |

---

## 🚀 DEPLOYMENT READINESS COMMANDS

| **DEPLOY COMMAND** | **DEPLOYMENT TASK** |
|-------------------|---------------------|
| `Prepare production build with minification and optimization` | Prepare production build với minification và optimization |
| `Configure production server with proper security settings` | Configure production server với proper security settings |
| `Setup monitoring and analytics for deployed PWA` | Setup monitoring và analytics cho deployed PWA |
| `Generate user documentation and installation guide` | Tạo user documentation và installation guide |
| `Confirm successful deployment with live testing` | Confirm successful deployment với live testing |