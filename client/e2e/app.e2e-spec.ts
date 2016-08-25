import { DixitOnlineClientPage } from './app.po';

describe('dixit-online-client App', function() {
  let page: DixitOnlineClientPage;

  beforeEach(() => {
    page = new DixitOnlineClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
