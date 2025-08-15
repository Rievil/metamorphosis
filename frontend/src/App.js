import React, { useState, useEffect } from 'https://esm.sh/react@18';
import api from './apiClient.js';

const tabs = ['Sessions', 'World Environments', 'Archetypes', 'Skills'];

function SessionsTab() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ user_id: '', token: '' });

  useEffect(() => {
    api.listSessions().then(setItems).catch(console.error);
  }, []);

  const submit = (e) => {
    e.preventDefault();
    api
      .createSession({ user_id: Number(form.user_id), token: form.token })
      .then((item) => {
        setItems((prev) => [...prev, item]);
        setForm({ user_id: '', token: '' });
      })
      .catch(console.error);
  };

  return React.createElement(
    'div',
    null,
    React.createElement(
      'ul',
      { className: 'mb-4' },
      items.map((s) =>
        React.createElement('li', { key: s.id }, `${s.id}: ${s.token}`)
      )
    ),
    React.createElement(
      'form',
      { onSubmit: submit, className: 'flex flex-col gap-2' },
      React.createElement('input', {
        placeholder: 'User ID',
        value: form.user_id,
        onChange: (e) => setForm({ ...form, user_id: e.target.value }),
      }),
      React.createElement('input', {
        placeholder: 'Token',
        value: form.token,
        onChange: (e) => setForm({ ...form, token: e.target.value }),
      }),
      React.createElement('button', { type: 'submit' }, 'Create')
    )
  );
}

function WorldEnvironmentsTab() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ name: '', climate: '', description: '' });

  useEffect(() => {
    api.listWorldEnvironments().then(setItems).catch(console.error);
  }, []);

  const submit = (e) => {
    e.preventDefault();
    api
      .createWorldEnvironment(form)
      .then((item) => {
        setItems((prev) => [...prev, item]);
        setForm({ name: '', climate: '', description: '' });
      })
      .catch(console.error);
  };

  return React.createElement(
    'div',
    null,
    React.createElement(
      'ul',
      { className: 'mb-4' },
      items.map((w) =>
        React.createElement(
          'li',
          { key: w.id },
          `${w.name} (${w.climate || 'n/a'})`
        )
      )
    ),
    React.createElement(
      'form',
      { onSubmit: submit, className: 'flex flex-col gap-2' },
      React.createElement('input', {
        placeholder: 'Name',
        value: form.name,
        onChange: (e) => setForm({ ...form, name: e.target.value }),
      }),
      React.createElement('input', {
        placeholder: 'Climate',
        value: form.climate,
        onChange: (e) => setForm({ ...form, climate: e.target.value }),
      }),
      React.createElement('input', {
        placeholder: 'Description',
        value: form.description,
        onChange: (e) => setForm({ ...form, description: e.target.value }),
      }),
      React.createElement('button', { type: 'submit' }, 'Create')
    )
  );
}

function ArchetypesTab() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ name: '', description: '' });

  useEffect(() => {
    api.listArchetypes().then(setItems).catch(console.error);
  }, []);

  const submit = (e) => {
    e.preventDefault();
    api
      .createArchetype(form)
      .then((item) => {
        setItems((prev) => [...prev, item]);
        setForm({ name: '', description: '' });
      })
      .catch(console.error);
  };

  return React.createElement(
    'div',
    null,
    React.createElement(
      'ul',
      { className: 'mb-4' },
      items.map((a) =>
        React.createElement('li', { key: a.id }, a.name)
      )
    ),
    React.createElement(
      'form',
      { onSubmit: submit, className: 'flex flex-col gap-2' },
      React.createElement('input', {
        placeholder: 'Name',
        value: form.name,
        onChange: (e) => setForm({ ...form, name: e.target.value }),
      }),
      React.createElement('input', {
        placeholder: 'Description',
        value: form.description,
        onChange: (e) => setForm({ ...form, description: e.target.value }),
      }),
      React.createElement('button', { type: 'submit' }, 'Create')
    )
  );
}

function SkillsTab() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({
    name: '',
    description: '',
    archetype_id: '',
  });

  useEffect(() => {
    api.listSkills().then(setItems).catch(console.error);
  }, []);

  const submit = (e) => {
    e.preventDefault();
    const payload = {
      ...form,
      archetype_id: form.archetype_id ? Number(form.archetype_id) : null,
    };
    api
      .createSkill(payload)
      .then((item) => {
        setItems((prev) => [...prev, item]);
        setForm({ name: '', description: '', archetype_id: '' });
      })
      .catch(console.error);
  };

  return React.createElement(
    'div',
    null,
    React.createElement(
      'ul',
      { className: 'mb-4' },
      items.map((s) => React.createElement('li', { key: s.id }, s.name))
    ),
    React.createElement(
      'form',
      { onSubmit: submit, className: 'flex flex-col gap-2' },
      React.createElement('input', {
        placeholder: 'Name',
        value: form.name,
        onChange: (e) => setForm({ ...form, name: e.target.value }),
      }),
      React.createElement('input', {
        placeholder: 'Description',
        value: form.description,
        onChange: (e) => setForm({ ...form, description: e.target.value }),
      }),
      React.createElement('input', {
        placeholder: 'Archetype ID',
        value: form.archetype_id,
        onChange: (e) => setForm({ ...form, archetype_id: e.target.value }),
      }),
      React.createElement('button', { type: 'submit' }, 'Create')
    )
  );
}

export default function App() {
  const [active, setActive] = useState(tabs[0]);

  return React.createElement(
    'div',
    { className: 'min-h-screen bg-white text-black flex flex-col' },
    React.createElement(
      'nav',
      { className: 'border-b border-black flex flex-wrap' },
      tabs.map((tab) =>
        React.createElement(
          'button',
          {
            key: tab,
            onClick: () => setActive(tab),
            className: `px-4 py-2 transition-colors ${
              active === tab ? 'bg-black text-white' : 'hover:bg-gray-200'
            }`,
          },
          tab
        )
      )
    ),
    React.createElement(
      'main',
      { className: 'p-4 flex-grow' },
      active === 'Sessions' && React.createElement(SessionsTab),
      active === 'World Environments' && React.createElement(WorldEnvironmentsTab),
      active === 'Archetypes' && React.createElement(ArchetypesTab),
      active === 'Skills' && React.createElement(SkillsTab)
    )
  );
}
