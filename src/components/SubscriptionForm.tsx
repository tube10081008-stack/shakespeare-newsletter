'use client';

import { useState } from 'react';
import styles from './Hero.module.css'; // Reusing Hero styles for consistency

export default function SubscriptionForm() {
    const [email, setEmail] = useState('');
    const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus('loading');

        try {
            const res = await fetch('/api/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email }),
            });

            if (!res.ok) throw new Error('Subscription failed');

            setStatus('success');
            setEmail('');
        } catch (error) {
            console.error(error);
            setStatus('error');
            alert('구독 신청 중 오류가 발생했습니다. 다시 시도해주세요.');
        } finally {
            if (status !== 'success') setStatus('idle');
        }
    };

    if (status === 'success') {
        return (
            <div className={styles.successMessage} style={{ color: 'var(--color-secondary)', fontSize: '1.2rem', marginTop: '1rem', animation: 'fadeIn 0.5s' }}>
                ✨ 환영합니다! 당신의 이름이 명부에 기록되었습니다.
            </div>
        );
    }

    return (
        <form className={styles.ctaContainer} onSubmit={handleSubmit}>
            <input
                type="email"
                placeholder="이메일 주소를 입력하세요"
                className={styles.input}
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={status === 'loading'}
            />
            <button
                type="submit"
                className={styles.button}
                disabled={status === 'loading'}
                style={{ opacity: status === 'loading' ? 0.7 : 1, cursor: status === 'loading' ? 'wait' : 'pointer' }}
            >
                {status === 'loading' ? '기록하는 중...' : '여정 시작하기'}
            </button>
        </form>
    );
}
