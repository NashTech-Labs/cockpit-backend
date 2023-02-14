import { ReverseListPipe } from './reverse-list.pipe';

describe('ReverseList', () => {
    let pipe: ReverseListPipe;
    const mockList = [1, 2, 3];

    beforeEach(() => {
        pipe = new ReverseListPipe();
    });

    it('it should show filtered list of employees', () => {
        expect(pipe.transform(mockList)[0]).toEqual(mockList[2]);
    });
});
