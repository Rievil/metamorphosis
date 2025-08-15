import React, { useState, useEffect } from 'https://esm.sh/react@18';
import api from './apiClient.js';

const tabs = ['Sessions', 'World', 'Players', 'Archetypes'];

export default function App() {
  const [active, setActive] = useState(tabs[0]);

  useEffect(() => {
    const loaders = {
      Sessions: api.getSessions,
      World: api.getWorld,
      Players: api.getPlayers,
      Archetypes: api.getArchetypes,
    };
    loaders[active]()
      .then((data) => console.log(`${active} data`, data))
      .catch((err) => console.error(err));
  }, [active]);

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
      active === 'Sessions' && React.createElement('div', null, 'Sessions content'),
      active === 'World' && React.createElement('div', null, 'World content'),
      active === 'Players' && React.createElement('div', null, 'Players content'),
      active === 'Archetypes' && React.createElement('div', null, 'Archetypes content')
    )
  );
}
