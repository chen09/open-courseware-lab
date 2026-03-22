#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const repoRoot = process.cwd();
const manifestPath = path.join(repoRoot, "lessons", "manifest.json");
const reportDir = path.join(repoRoot, "reports", "workflow-audit");
const reportPath = path.join(reportDir, "latest.json");

const requiredMetaFields = [
  "id",
  "title",
  "subject",
  "gradeBand",
  "topic",
  "slug",
  "entry",
  "assets",
  "features",
];

const featureContracts = {
  "tabs:problem-solution-animation": {
    type: "all-keywords",
    keywords: ["problem", "solution", "animation"],
  },
  "teacher-mode": {
    type: "any-keyword",
    keywords: ["teacher-mode", "teacher mode", "teacher"],
  },
  "multilingual:ja-zh-en": {
    type: "multilingual",
  },
  "auto-language-rotation": {
    type: "any-keyword",
    keywords: ["auto-language", "language-rotation", "auto rotate", "rotation"],
  },
  "timeline-animation": {
    type: "any-keyword",
    keywords: ["timeline", "time slider", "input type=\"range\""],
  },
  "cross-validation-matrix": {
    type: "any-keyword",
    keywords: ["cross-validation", "validation matrix", "double check"],
  },
  "manim-explainer-slot": {
    type: "any-keyword",
    keywords: ["assets/explain", "scene-01.mp4", "manim"],
  },
};

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function exists(filePath) {
  return fs.existsSync(filePath);
}

function normalizeText(text) {
  return text.toLowerCase();
}

function checkFeatureContract(feature, indexText, meta, result) {
  const contract = featureContracts[feature];
  if (!contract) {
    result.warnings.push(`Unknown feature contract: ${feature}`);
    return;
  }

  if (contract.type === "multilingual") {
    const title = meta?.title ?? {};
    const hasMetaLocales = Boolean(title.ja && title.zh && title.en);
    const hasIndexLocales =
      indexText.includes("ja") && indexText.includes("zh") && indexText.includes("en");
    if (!hasMetaLocales || !hasIndexLocales) {
      result.errors.push(
        `Feature mismatch for multilingual:ja-zh-en (meta/locales missing in ${result.lessonPath})`,
      );
    }
    return;
  }

  if (contract.type === "all-keywords") {
    const missing = contract.keywords.filter((k) => !indexText.includes(k));
    if (missing.length > 0) {
      result.warnings.push(
        `Feature check weak signal for ${feature} in ${result.lessonPath}; missing keywords: ${missing.join(", ")}`,
      );
    }
    return;
  }

  if (contract.type === "any-keyword") {
    const matched = contract.keywords.some((k) => indexText.includes(k));
    if (!matched) {
      result.warnings.push(
        `Feature check weak signal for ${feature} in ${result.lessonPath}; none of keywords matched`,
      );
    }
  }
}

function main() {
  const report = {
    generatedAt: new Date().toISOString(),
    status: "PASS",
    errors: [],
    warnings: [],
    lessons: [],
  };

  if (!exists(manifestPath)) {
    report.status = "BLOCKED";
    report.errors.push(`Missing manifest: ${manifestPath}`);
    writeReportAndExit(report, 1);
  }

  const manifest = readJson(manifestPath);
  if (!Array.isArray(manifest.lessons)) {
    report.status = "BLOCKED";
    report.errors.push("Invalid manifest format: lessons must be an array");
    writeReportAndExit(report, 1);
  }

  if (manifest.count !== manifest.lessons.length) {
    report.errors.push(
      `Manifest count mismatch: count=${manifest.count}, lessons.length=${manifest.lessons.length}`,
    );
  }

  for (const lesson of manifest.lessons) {
    const lessonPath = path.join(repoRoot, lesson.path ?? "");
    const lessonResult = {
      id: lesson.id,
      lessonPath: lesson.path,
      errors: [],
      warnings: [],
    };

    if (!exists(lessonPath)) {
      lessonResult.errors.push(`Lesson directory not found: ${lesson.path}`);
      report.lessons.push(lessonResult);
      continue;
    }

    const metaPath = path.join(lessonPath, "meta.json");
    const indexPath = path.join(lessonPath, lesson.entry ?? "index.html");

    if (!exists(metaPath)) {
      lessonResult.errors.push(`Missing meta.json at ${lesson.path}`);
      report.lessons.push(lessonResult);
      continue;
    }

    if (!exists(indexPath)) {
      lessonResult.errors.push(`Missing entry file at ${lesson.path}${lesson.entry}`);
      report.lessons.push(lessonResult);
      continue;
    }

    const meta = readJson(metaPath);
    const indexText = normalizeText(fs.readFileSync(indexPath, "utf8"));

    for (const field of requiredMetaFields) {
      if (meta[field] === undefined || meta[field] === null) {
        lessonResult.errors.push(`meta.json missing required field: ${field}`);
      }
    }

    if (lesson.id !== meta.id) {
      lessonResult.errors.push(`ID mismatch: manifest(${lesson.id}) != meta(${meta.id})`);
    }

    for (const asset of lesson.assets ?? []) {
      const assetPath = path.join(lessonPath, asset);
      if (!exists(assetPath)) {
        lessonResult.errors.push(`Missing asset: ${path.join(lesson.path, asset)}`);
      }
    }

    for (const feature of lesson.features ?? []) {
      checkFeatureContract(feature, indexText, meta, lessonResult);
    }

    report.lessons.push(lessonResult);
  }

  const rootIndexPath = path.join(repoRoot, "index.html");
  if (exists(rootIndexPath)) {
    const rootIndexText = fs.readFileSync(rootIndexPath, "utf8");
    const hasCatalogTitle = rootIndexText.includes("Open Courseware Lab");
    const hasLegacyTitle = rootIndexText.includes("Jiro Taro Motion Demo");
    if (hasCatalogTitle && hasLegacyTitle) {
      report.warnings.push(
        "Root index contains both catalog and legacy lesson markers; verify runtime dual-state risk.",
      );
    }
  } else {
    report.errors.push("Missing root index.html");
  }

  for (const lessonResult of report.lessons) {
    report.errors.push(...lessonResult.errors);
    report.warnings.push(...lessonResult.warnings);
  }

  if (report.errors.length > 0) {
    report.status = "BLOCKED";
  } else if (report.warnings.length > 0) {
    report.status = "PASS_WITH_WARNINGS";
  }

  const exitCode = report.status === "BLOCKED" ? 1 : 0;
  writeReportAndExit(report, exitCode);
}

function writeReportAndExit(report, exitCode) {
  fs.mkdirSync(reportDir, { recursive: true });
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + "\n", "utf8");
  console.log(`Workflow audit report written to ${path.relative(repoRoot, reportPath)}`);
  console.log(`Status: ${report.status}`);
  console.log(`Errors: ${report.errors.length}`);
  console.log(`Warnings: ${report.warnings.length}`);
  process.exit(exitCode);
}

main();
