import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const DATA_DIR = path.join(process.cwd(), 'src', 'data');
const SUBSCRIBERS_FILE = path.join(DATA_DIR, 'subscribers.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

export async function POST(request: Request) {
    try {
        const { email } = await request.json();

        if (!email || !email.includes('@')) {
            return NextResponse.json(
                { error: 'Invalid email address' },
                { status: 400 }
            );
        }

        // Read existing subscribers
        let subscribers: string[] = [];
        if (fs.existsSync(SUBSCRIBERS_FILE)) {
            const data = fs.readFileSync(SUBSCRIBERS_FILE, 'utf-8');
            try {
                subscribers = JSON.parse(data);
            } catch (e) {
                subscribers = [];
            }
        }

        // Add new subscriber if not exists
        if (!subscribers.includes(email)) {
            subscribers.push(email);
            fs.writeFileSync(SUBSCRIBERS_FILE, JSON.stringify(subscribers, null, 2));
            console.log(`[DB] Saved Subscriber: ${email}`);
        } else {
            console.log(`[DB] Subscriber already exists: ${email}`);
        }

        return NextResponse.json({ success: true, message: 'Subscribed successfully' });
    } catch (error) {
        console.error('Subscription Error:', error);
        return NextResponse.json(
            { error: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
