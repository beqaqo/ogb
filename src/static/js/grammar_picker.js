const picker = document.getElementById('grammar-picker');
const input = document.getElementById('q_grammar');
const list = document.getElementById('grammar-options');
const allTags = JSON.parse(document.getElementById('grammar-data').textContent);


function startsWith(tag, prefix) {
  return tag.toLowerCase().startsWith(prefix.toLowerCase());
}

// Split the input at the last dot:
//   "V.Aor.in"  ->  parent = "V.Aor.",  typed = "in"
function splitInput(text) {
  const lastDot = text.lastIndexOf('.');
  return {
    parent: text.slice(0, lastDot + 1),
    typed: text.slice(lastDot + 1).toLowerCase(),
  };
}

// Find every possible next part of a tag.
function findOptions(parent, typed) {
  const options = new Set();

  for (const tag of allTags) {
    if (!startsWith(tag, parent)) continue;

    const nextPart = tag.slice(parent.length).split('.')[0];
    if (nextPart.toLowerCase().includes(typed)) {
      options.add(nextPart);
    }
  }

  return [...options].sort();
}

// Called when the user clicks an option
function choose(parent, option) {
  const value = parent + option;

  // add a dot only if the tag continues, so the next level shows up
  const hasNextLevel = allTags.some((tag) => startsWith(tag, value + '.'));
  input.value = hasNextLevel ? value + '.' : value;

  input.focus();
  showOptions();
}

// Build the dropdown
function showOptions() {
  const { parent, typed } = splitInput(input.value);
  const options = findOptions(parent, typed);

  list.innerHTML = '';

  for (const option of options) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'list-group-item list-group-item-action py-1 form-control-custom rounded-0';
    button.textContent = option;
    button.addEventListener('click', () => choose(parent, option));
    list.appendChild(button);
  }

  // hide the dropdown when there is nothing to show
  list.classList.toggle('d-none', options.length === 0);
}


input.addEventListener('input', showOptions);
input.addEventListener('focus', showOptions);

// click anywhere outside -> close the dropdown
document.addEventListener('mousedown', (event) => {
  if (!picker.contains(event.target)) {
    list.classList.add('d-none');
  }
});