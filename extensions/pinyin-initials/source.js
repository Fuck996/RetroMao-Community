retromao.define({
  actions: {
    initials({ texts }) {
      return { aliases: texts.map(text => {
        const value = pinyinPro.pinyin(text, { type: 'all', toneType: 'none', traditional: true })
          .map(part => part.isZh ? part.first : part.origin).join('')
          .toLowerCase().replace(/[\s\p{P}]/gu, '');
        return value ? [value] : [];
      }) };
    }
  }
});
