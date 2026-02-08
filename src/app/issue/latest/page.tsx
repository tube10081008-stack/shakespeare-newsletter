'use client';

import { useEffect, useState } from 'react';
import styles from './issue.module.css';
import Link from 'next/link';

interface IssueData {
    meta: {
        date: string;
        theme: string;
    };
    main_quote: string;
    source: string;
    insight: string;
    second_act: string;
    weekly_preview: string;
}

export default function LatestIssuePage() {
    const [data, setData] = useState<IssueData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetch('/api/issue/latest')
            .then(res => {
                if (!res.ok) throw new Error('Failed to load issue');
                return res.json();
            })
            .then(data => {
                setData(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    const handleGenerate = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/issue/daily', { method: 'POST' });
            const result = await res.json();
            if (result.success) {
                setData(result.data);
            } else {
                alert('Generation failed: ' + result.error);
            }
        } catch (e) {
            alert('Error triggering generation');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div style={{ padding: '4rem', textAlign: 'center', color: 'white' }}>
                <p style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>📜</p>
                <p>잉크가 마르기를 기다리는 중... (AI가 집필 중입니다)</p>
                <p style={{ fontSize: '0.8rem', color: '#888', marginTop: '1rem' }}>약 30~60초가 소요될 수 있습니다.</p>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div style={{ padding: '4rem', textAlign: 'center', color: 'red' }}>
                ❌ 이슈를 불러올 수 없습니다. 다시 시도해주세요.
            </div>
        );
    }

    return (
        <main style={{ minHeight: '100vh', padding: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', maxWidth: '800px', margin: '0 auto' }}>
                <Link href="/" className={styles.backButton}>← 홈으로 돌아가기</Link>
                <button
                    onClick={handleGenerate}
                    style={{
                        background: 'var(--color-secondary)',
                        border: 'none',
                        padding: '0.5rem 1rem',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        marginBottom: '2rem',
                        color: '#fff'
                    }}
                >
                    새로운 이슈 발행하기 (AI)
                </button>
            </div>

            <article className={styles.container}>
                <header className={styles.header}>
                    <span className={styles.date}>{data.meta?.date} • {data.meta?.theme}</span>
                    <h1 className={styles.title}>The Daily Bard</h1>
                </header>

                <section className={styles.quoteSection}>
                    <p className={styles.quote}>"{data.main_quote}"</p>
                    <cite className={styles.source}>— {data.source}</cite>
                </section>

                <section>
                    <h2 className={styles.sectionTitle}>💡 Insight (깊이 읽기)</h2>
                    <p className={styles.text}>{data.insight}</p>
                </section>

                <section>
                    <h2 className={styles.sectionTitle}>🎭 Second Act (다른 시선)</h2>
                    <p className={styles.text}>{data.second_act}</p>
                </section>

                <section>
                    <h2 className={styles.sectionTitle}>📅 Next Theme</h2>
                    <p className={styles.text}>{data.weekly_preview}</p>
                </section>

                <footer className={styles.footer}>
                    <p>Shakespeare's Chronicle • Daily Wisdom</p>
                </footer>
            </article>
        </main>
    );
}
