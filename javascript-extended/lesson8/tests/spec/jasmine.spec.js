describe('Соответствие значений', () => {
   it('Проверка a на значение 10', () => {
       let a = 10; // то, что мы тестируем
       expect(a).toBe(10);

       expect(a).not.toBe(9);
   });
   it('Сравнение объектов', () => {
       let user1 = {
           name: 'Ann',
           age: 20
       };
       let user2 = {
           name: 'Ann',
           age: 20
       };
       // await pow();
       expect(user1).toEqual(user2);


       // expect(user1).not.toBeNull();
       // expect(user1).toBeUndefined();
       // expect(user1).toBeNaN();
       // expect(user1).toBeTruthy();
       // expect(user1).toBeFalsy();
       // expect(user1).toBeGreaterThan();
       // expect(user1).toBeLessThan();
       // expect(user1).toBeGreaterThanOrEqual();
       // expect(user1).toBeLessThanOrEqual();
       // expect(user1).toBeCloseTo();


   });
    it('RegEx', () => {
        let str = 'Test AbcD jasmine'; // то, что мы тестируем
        expect(str).toMatch(/abcd/i);
        expect(str).not.toMatch(/abcd/);
    });
    it('Array', () => {
        let arr = ['white', 'black']; // то, что мы тестируем
        expect(arr).toContain('black');
        expect(arr).not.toContain('pink');
    });
});