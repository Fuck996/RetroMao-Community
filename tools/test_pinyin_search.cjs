const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const source = path.join(__dirname, '../extensions/pinyin-initials');
const script = fs.readFileSync(path.join(source, 'main.js'), 'utf8');
let actions;
vm.runInNewContext(script, { retromao: { define(value) { actions = value.actions; } } });

test('offline initials cover simplified traditional mixed text and contextual pronunciation', () => {
  const texts = ['魂斗罗', '計算器', '计算器', '重庆', '超级 Mario 64', '魂斗罗（美版）.zip', '...'];
  const result = JSON.parse(JSON.stringify(actions.initials({ texts })));
  assert.deepEqual(result.aliases, [['hdl'], ['jsq'], ['jsq'], ['cq'], ['cjmario64'], ['hdlmbzip'], []]);
  assert.equal(result.aliases.length, texts.length);
});

test('bundle is reproducible from pinned offline dependencies and fits host limits', () => {
  const vendor = path.join(source, 'vendor');
  const lock = JSON.parse(fs.readFileSync(path.join(vendor, 'manifest.json')));
  for (const [file, hash] of Object.entries(lock.files)) {
    assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(vendor, file))).digest('hex'), hash);
  }
  const expected = fs.readFileSync(path.join(vendor, 'pinyin-pro.js'), 'utf8') + '\npinyinPro.addTraditionalDict(' +
    JSON.stringify(JSON.parse(fs.readFileSync(path.join(vendor, 'traditional.json')))) + ');\n' + fs.readFileSync(path.join(source, 'source.js'), 'utf8');
  assert.equal(script, expected);
  assert.ok(Buffer.byteLength(script) < 4 * 1024 * 1024);
  const result = actions.initials({ texts: Array.from({ length: 200 }, () => '魂斗罗') });
  assert.ok(Buffer.byteLength(JSON.stringify(result)) < 512 * 1024);
});
