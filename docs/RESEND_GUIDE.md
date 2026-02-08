# 📧 Resend 이메일 인증 가이드

 Resend의 무료(Sandbox) 플랜 정책상, 수신자 추가 방식이 엄격합니다. "Add Email" 버튼이 없는 것은 정상입니다.

## 1. Sandbox에서 테스트하기 (나에게만 발송)
Sandbox 모드에서는 **계정을 생성할 때 사용한 본인 이메일**로만 발송이 가능합니다.
- 예: `tube1@gmail.com`으로 가입했다면, 받는 사람(To)을 `tube1@gmail.com`으로 설정해야만 발송됩니다.
- 별도의 버튼으로 추가하는 것이 아니라, 그냥 그 주소로 보내면 됩니다.

## 2. 다른 사람에게 보내려면? (도메인 인증 필수)
다른 사람(`friend@naver.com` 등)에게 보내려면 반드시 **도메인 인증**을 해야 합니다.
1.  좌측 메뉴의 **Domains**를 클릭합니다.
2.  **Add Domain**을 클릭합니다.
3.  보유하신 도메인(예: `daily-bard.com`)을 입력합니다. (도메인이 없다면 구매가 필요합니다.)
4.  나타나는 DNS 레코드를 도메인 관리 사이트에 입력합니다.
5.  인증이 완료되면(`Verified`), 이제 **누구에게나** 이메일을 보낼 수 있는 제한이 풀립니다.

## 요약
- **내 이메일로 테스트**: 별도 설정 불필요. 가입한 이메일로 보내면 됨.
- **남에게 발송**: `Domains` 메뉴에서 도메인 연결 필수.


## 2. 도메인 인증하기 (발신자 인증 - 권장)
`onboarding@resend.dev` 대신 `newsletter@daily-shakespeare.site` 처럼 멋진 도메인으로 보내려면:

1.  **Resend Dashboard > Domains > Add Domain** 클릭.
2.  `daily-shakespeare.site` 입력 후 **Add**.
3.  화면에 **DNS Records** (MX, TXT)가 나옵니다. 이 값을 도메인 관리 페이지에 "복사-붙여넣기" 해야 합니다.

### 💡 도메인 관리 페이지 입력 방법
보내주신 화면(가비아/호스팅KR 등)의 입력칸에 이렇게 넣으세요:

**[공통]**
*   **TTL**: 600 (그대로 두세요)
*   **추가/확인 버튼**: 입력 후 반드시 '추가' 또는 '확인'을 눌러야 저장됩니다.

**1. MX 레코드 (메일 수신용)**
*   **타입**: `MX` 선택
*   **호스트**: Resend의 `Name` 값 (보통 `bounces` 또는 `@`)
*   **값/위치**: Resend의 `Value` 값 (예: `feedback-smtp.us-east-1.amazonses.com`)
*   **우선순위**: `10`

**2. TXT 레코드 (SPF/DKIM 인증 - 가장 중요!)**
*   **타입**: `TXT` 선택
*   **호스트**: Resend의 `Name` 값 (예: `bounces` 또는 `resend._domainkey`)
*   **값/위치**: Resend의 `Value` 값 (예: `v=spf1 include:...` 또는 `p=MIGf...`)
*   **우선순위**: (비워둠)

**주의사항:**
*   **호스트(Name)** 입력 시, `bounces.daily-shakespeare.site` 처럼 전체가 나오더라도, 입력칸에는 `bounces`만 넣어야 할 수 있습니다. (자동으로 뒤에 도메인이 붙는 경우가 많음)
*   입력 후 **Verify Status** 버튼을 눌러 `Verified`가 뜰 때까지 기다리세요 (최대 48시간, 보통 10분 내 완료).
