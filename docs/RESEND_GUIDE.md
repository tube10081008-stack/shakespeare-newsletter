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


## 2. Domain 인증하기 (발신자 인증 - 권장)
`onboarding@resend.dev` 대신 `newsletter@myproject.com` 처럼 멋진 도메인으로 보내려면:
1.  [Resend Dashboard - Domains](https://resend.com/domains) 페이지로 이동합니다.
2.  **Add Domain**을 클릭하고 보유한 도메인(예: `daily-bard.com`)을 입력합니다.
3.  화면에 나오는 **DNS 레코드(DKIM, SPF 등)**를 도메인 관리 사이트(가비아, GoDaddy, AWS Route53 등)에 입력합니다.
4.  설정이 완료되면 `Status: Verified`가 뜹니다.
5.  이제 `.env` 파일의 `SENDER_EMAIL`을 `Shakespeare <hello@daily-bard.com>` 등으로 변경할 수 있습니다.
