import styles from './Features.module.css';

const features = [
    {
        title: "매일의 지혜",
        description: "당신의 아침을 깨우는 셰익스피어의 문장. 영감과 위로, 때로는 깊은 울림을 전합니다.",
        icon: "📜"
    },
    {
        title: "현대적 해석",
        description: "고전의 맥락과 의미를 현대적으로 풀어낸 깊이 있는 통찰을 만나보세요.",
        icon: "🧠"
    },
    {
        title: "당신을 위한 무대",
        description: "셰익스피어의 유산을 이어가는 학자, 배우, 그리고 애호가들의 커뮤니티에 참여하세요.",
        icon: "🎭"
    }
];

export default function Features() {
    return (
        <section className={styles.container}>
            <h2 className={styles.heading}>구독해야 하는 이유</h2>
            <div className={styles.grid}>
                {features.map((feature, index) => (
                    <div key={index} className={styles.card}>
                        <div className={styles.icon}>{feature.icon}</div>
                        <h3 className={styles.title}>{feature.title}</h3>
                        <p className={styles.description}>{feature.description}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}
