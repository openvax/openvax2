"use strict";

const map = document.getElementById("package-map");
const detail = document.getElementById("package-detail");
const search = document.getElementById("package-search");
const status = document.getElementById("search-status");
const empty = document.getElementById("empty-search");
let packages = [];
let selected = "vaxrank";

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function link(text, url) {
  const node = element("a", "", text);
  node.href = url;
  return node;
}

function relatedList(names, fallback) {
  const list = element("div", "related-packages");
  if (!names.length) list.append(element("p", "", fallback));
  for (const name of names) {
    const button = element("button", "", name);
    button.type = "button";
    button.addEventListener("click", () => selectPackage(name));
    list.append(button);
  }
  return list;
}

function renderDetail() {
  const pkg = packages.find(item => item.id === selected);
  const consumers = packages.filter(item => item.dependencies.includes(selected));
  const title = element("h3", "", pkg.label);
  title.id = "detail-name";
  title.tabIndex = -1;
  const io = element("dl");
  io.append(element("dt", "", "Takes in"), element("dd", "", pkg.input),
    element("dt", "", "Provides"), element("dd", "", pkg.output));
  const links = element("div", "detail-links");
  links.append(link("Repository & docs", pkg.repository),
    link("PyPI package", `https://pypi.org/project/${pkg.id}/`));
  detail.replaceChildren(element("p", "detail-category", pkg.category), title,
    element("p", "", pkg.summary), io, element("p", "boundary", pkg.boundary),
    element("h4", "", "Depends on in this map"),
    relatedList(pkg.dependencies, "No direct dependencies among the mapped packages."),
    element("h4", "", "Used by in this map"),
    relatedList(consumers.map(item => item.id), "No direct consumers among the mapped packages."), links);
}

function renderMap() {
  const query = search.value.trim().toLowerCase();
  const selection = packages.find(item => item.id === selected);
  const matches = packages.filter(pkg => [pkg.id, pkg.label, pkg.tagline, pkg.category,
    pkg.summary, pkg.input, pkg.output].join(" ").toLowerCase().includes(query));
  map.replaceChildren();
  const groups = [...new Set(packages.map(pkg => pkg.category))];
  for (const group of groups) {
    const members = matches.filter(pkg => pkg.category === group);
    if (!members.length) continue;
    const section = element("section", "package-group");
    section.append(element("h3", "", group));
    const nodes = element("div");
    for (const pkg of members) {
      let relation = "";
      let state = "";
      if (pkg.id === selected) { relation = "Selected"; state = "is-selected"; }
      else if (selection.dependencies.includes(pkg.id)) { relation = "Dependency"; state = "is-dependency"; }
      else if (pkg.dependencies.includes(selected)) { relation = "Consumer"; state = "is-consumer"; }
      const button = element("button", `package-node ${state}`);
      button.type = "button";
      button.dataset.package = pkg.id;
      button.setAttribute("aria-pressed", String(pkg.id === selected));
      button.setAttribute("aria-controls", "package-detail");
      button.append(element("strong", "", pkg.label), element("span", "node-task", pkg.tagline));
      if (relation) button.append(element("span", "relation-tag", relation));
      button.addEventListener("click", () => selectPackage(pkg.id));
      nodes.append(button);
    }
    section.append(nodes);
    map.append(section);
  }
  status.textContent = `${matches.length} of ${packages.length} packages shown. Relationships for ${selection.label}.`;
  empty.hidden = matches.length !== 0;
}

function selectPackage(id, jump = false) {
  if (!packages.some(pkg => pkg.id === id)) return;
  const previousFocus = document.activeElement;
  const fromMap = previousFocus?.dataset?.package;
  const fromDetail = detail.contains(previousFocus);
  selected = id;
  renderMap();
  renderDetail();
  if (fromMap) map.querySelector(`[data-package="${id}"]`)?.focus({preventScroll: true});
  if (fromDetail || jump) document.getElementById("detail-name").focus({preventScroll: true});
  if (jump || window.matchMedia("(max-width: 850px)").matches) {
    detail.scrollIntoView({behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth", block: "start"});
  }
}

async function initialize() {
  try {
    const response = await fetch("packages.json");
    if (!response.ok) throw new Error("Package data unavailable");
    const data = await response.json();
    packages = data.packages;
    renderMap();
    renderDetail();
    search.disabled = false;
    search.addEventListener("input", renderMap);
    document.getElementById("clear-search").addEventListener("click", () => {
      search.value = "";
      renderMap();
      search.focus();
    });
    document.querySelectorAll("[data-select]").forEach(node => {
      node.addEventListener("click", event => {
        event.preventDefault();
        search.value = "";
        selectPackage(node.dataset.select, true);
      });
    });
  } catch (error) {
    status.textContent = "The interactive map could not load. Browse the package repositories below.";
    document.querySelector(".source-directory").open = true;
  }
}

initialize();
