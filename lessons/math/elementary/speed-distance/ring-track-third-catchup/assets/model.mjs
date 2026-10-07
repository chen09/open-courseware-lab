// All times are minutes from B's departure; all distances are metres.
export const MODEL = Object.freeze({ circumference: 3000, speedA: 300, speedB: 180, delay: 2, end: 55 });
export const EVENTS = Object.freeze([5, 30, 55]);
export function stateAt(time) {
  const t = Math.max(0, Math.min(MODEL.end, Number(time) || 0));
  const timeA = Math.max(0, t - MODEL.delay);
  const distanceA = MODEL.speedA * timeA;
  const distanceB = MODEL.speedB * t;
  const positionA = distanceA % MODEL.circumference;
  const positionB = distanceB % MODEL.circumference;
  const eventIndex = EVENTS.findIndex(event => Math.abs(t - event) < 1e-7);
  return { time: t, timeA, startedA: t >= MODEL.delay, distanceA, distanceB, positionA, positionB,
    lapsA: Math.floor(distanceA / MODEL.circumference), lapsB: Math.floor(distanceB / MODEL.circumference),
    catches: EVENTS.filter(event => t >= event - 1e-7).length, event: eventIndex + 1 };
}
export function pointAt(distance, radius = 135) {
  const angle = Math.PI + 2 * Math.PI * (distance % MODEL.circumference) / MODEL.circumference;
  return { x: 200 + radius * Math.cos(angle), y: 200 + radius * Math.sin(angle) };
}
