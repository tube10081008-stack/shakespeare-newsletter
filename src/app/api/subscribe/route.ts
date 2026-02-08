import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);
const AUDIENCE_ID = process.env.RESEND_AUDIENCE_ID;

export async function POST(request: Request) {
    try {
        const { email } = await request.json();

        if (!email || !email.includes('@')) {
            return NextResponse.json(
                { error: 'Invalid email address' },
                { status: 400 }
            );
        }

        if (!AUDIENCE_ID) {
            console.error('RESEND_AUDIENCE_ID is not defined');
            return NextResponse.json(
                { error: 'Server configuration error' },
                { status: 500 }
            );
        }

        try {
            await resend.contacts.create({
                email: email,
                firstName: '',
                lastName: '',
                unsubscribed: false,
                audienceId: AUDIENCE_ID,
            });
            console.log(`[Resend] Subscribed: ${email}`);
            return NextResponse.json({ success: true, message: 'Subscribed successfully' });
        } catch (error) {
            console.error('[Resend] Subscription Error:', error);
            // Resend throws if already exists, handle gracefully if needed, or just return success
            return NextResponse.json({ success: true, message: 'Subscribed successfully (or updated)' });
        }

    } catch (error) {
        console.error('Subscription Error:', error);
        return NextResponse.json(
            { error: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
