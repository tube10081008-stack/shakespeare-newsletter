import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    const dataPath = path.join(process.cwd(), 'src/data/latest_issue.json');

    try {
        if (!fs.existsSync(dataPath)) {
            return NextResponse.json({ error: 'No issue found' }, { status: 404 });
        }

        const fileContents = fs.readFileSync(dataPath, 'utf8');
        const data = JSON.parse(fileContents);

        return NextResponse.json(data);
    } catch (error) {
        return NextResponse.json({ error: 'Failed to read issue data' }, { status: 500 });
    }
}
