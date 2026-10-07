import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { MODEL, EVENTS, stateAt, pointAt } from '../lessons/math/elementary/speed-distance/ring-track-third-catchup/assets/model.mjs';

// Method A: B's initial lead plus the extra laps, timed from A's start.
const timesA = [1, 2, 3].map(n => (180 * 2 + (n - 1) * 3000) / (300 - 180));
// Method B: solve travelled-distance equations using B's departure as zero.
const timesB = [0, 1, 2].map(k => (300 * 2 + k * 3000) / (300 - 180));
assert.deepEqual(timesA, [3, 28, 53]);
assert.deepEqual(timesB, EVENTS);
const positions = [900, 2400, 900];
EVENTS.forEach((time, i) => {
  const s = stateAt(time);
  assert.equal(s.timeA, timesA[i]);
  assert.equal(s.distanceA - s.distanceB, i * 3000);
  assert.equal(s.positionA, positions[i]);
  assert.equal(s.positionB, positions[i]);
  assert.equal(s.event, i + 1);
  assert.equal(s.catches, i + 1);
});
let sampledStates = 0;
for (let i = 0; i <= 2200; i++) {
  const s = stateAt(i / 40);
  assert.ok(s.positionA >= 0 && s.positionA < 3000);
  assert.ok(s.positionB >= 0 && s.positionB < 3000);
  for (const distance of [s.distanceA, s.distanceB]) {
    const p = pointAt(distance);
    assert.ok(Math.abs(Math.hypot(p.x - 200, p.y - 200) - 135) < 1e-8);
  }
  assert.equal(s.catches, EVENTS.filter(t => t <= s.time).length);
  assert.ok(s.timeA <= s.time);
  sampledStates++;
}
assert.equal(stateAt(1).distanceA, 0);
assert.equal(stateAt(2).distanceB, 360);
assert.equal(stateAt(4.99).catches, 0);
assert.equal(stateAt(29.99).catches, 1);
assert.equal(stateAt(54.99).catches, 2);
assert.equal(stateAt(12).positionA, 0);
assert.equal(stateAt(55).distanceA, 15900);
assert.equal(stateAt(55).distanceB, 9900);
assert.equal(stateAt(55).lapsA, 5);
assert.equal(stateAt(55).lapsB, 3);
assert.equal(MODEL.circumference, 3 * 1000);
assert.equal(pointAt(0).x, 65);
assert.ok(pointAt(1).y < 200); // Clockwise from the left-hand start.
const root = new URL('../', import.meta.url);
const meta = JSON.parse(await readFile(new URL('lessons/math/elementary/speed-distance/ring-track-third-catchup/meta.json', root)));
const manifest = JSON.parse(await readFile(new URL('lessons/manifest.json', root)));
const entry = manifest.lessons.find(l => l.id === meta.id);
assert.ok(entry);
assert.deepEqual(entry.title, meta.title);
assert.equal(manifest.count, manifest.lessons.length);
for (const asset of meta.assets) await readFile(new URL(`lessons/math/elementary/speed-distance/ring-track-third-catchup/${asset}`, root));
console.log(JSON.stringify({ status: 'PASS', methods: 2, sampledStates, timesA, timesB, positions, final: stateAt(55) }, null, 2));
