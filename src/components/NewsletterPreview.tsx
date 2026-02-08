import styles from './NewsletterPreview.module.css';

export default function NewsletterPreview() {
    return (
        <section className={styles.container}>
            <div className={styles.content}>
                <h2 className={styles.heading}>미리 보는 뉴스레터</h2>
                <p className={styles.subtext}>매일 아침, 당신의 메일함으로 배달되는 예술 한 조각.</p>
            </div>

            <div className={styles.previewParams}>
                <div className={styles.card}>
                    <div className={styles.cardHeader}>
                        <span className={styles.date}>2026년 10월 24일</span>
                        <h3 className={styles.cardTitle}>자비의 본질 (The Quality of Mercy)</h3>
                    </div>
                    <div className={styles.cardBody}>
                        <p className={styles.quote}>
                            "자비는 강요되는 것이 아니다.<br />
                            마치 하늘에서 대지로 부드럽게 떨어지는<br />
                            단비와도 같은 것이다..."
                        </p>
                        <div className={styles.separator}></div>
                        <p className={styles.analysis}>
                            <strong>오늘의 단상:</strong> '베니스의 상인' 속 포샤의 간청은 단순한 법리가 아닌, 용서의 신성함을 이야기합니다. 엄격한 절대성의 세계에서 우리는 어떻게 은혜를 구할 수 있을까요?
                        </p>
                        <button className={styles.readMore}>전체 분석 읽기 →</button>
                    </div>
                </div>
            </div>
        </section>
    );
}
