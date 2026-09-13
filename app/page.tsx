import { LiveSessionDoor } from './live-session-door';
import { RocketStudio } from './rocket-studio';
import { SessionOpsPanels } from './session-ops-panels';

export default function Page() {
  return <>
    <RocketStudio />
    <LiveSessionDoor />
    <SessionOpsPanels />
  </>;
}
