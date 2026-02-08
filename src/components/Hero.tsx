import styles from './Hero.module.css';
import SubscriptionForm from './SubscriptionForm';

export default function Hero() {
    return (
        <section className={styles.hero}>
            <div className={styles.content}>
                <h1 className={styles.title}>
                    셰익스피어,<br />매일 당신에게 말을 걸다
                </h1>
                <p className={styles.subtitle}>
                    셰익스피어의 희곡 전집에서 엄선한 지혜와 해학, 그리고 비극을<br />
                    현대적 시각으로 재해석하여 매일 보내드립니다.
                </p>

                <SubscriptionForm />
            </div>
        </section>
    );
}
