import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';
import util from 'util';
import fs from 'fs';

const execPromise = util.promisify(exec);

export async function POST() {
    try {
        const scriptPath = path.join(process.cwd(), 'scripts/generate_issue.py');

        // Command to run the python script
        // Attempt to use 'python' or 'python3' - assuming it's in path
        const command = `python "${scriptPath}"`;

        console.log(`Executing: ${command}`);

        const { stdout, stderr } = await execPromise(command);

        if (stderr) {
            console.error('Script Error:', stderr);
        }

        console.log('Script Output:', stdout);

        // Read the newly generated file
        const dataPath = path.join(process.cwd(), 'src/data/latest_issue.json');
        if (fs.existsSync(dataPath)) {
            const fileContents = fs.readFileSync(dataPath, 'utf8');
            const data = JSON.parse(fileContents);
            return NextResponse.json({ success: true, data });
        } else {
            return NextResponse.json({ error: 'Generation finished but file not found' }, { status: 500 });
        }

    } catch (error: any) {
        console.error('Generation Failed:', error);
        return NextResponse.json({
            error: 'Failed to generate issue',
            details: error.message
        }, { status: 500 });
    }
}
