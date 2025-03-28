import java.io.ByteArrayInputStream;
import static org.junit.Assert.*;
import org.junit.Test;

public class DemoTest {

    @Test
    public void validtriangle3() {
        assertTrue(Demo.isTriangle(3,4,5));
    }
    
    @Test
    public void onetwothree() {
        assertFalse(Demo.isTriangle(1, 2, 3));
    }

    @Test
    public void validtriangle4() {
        assertTrue(Demo.isTriangle(4,5,3));
    }

    @Test
    public void validtriangle5() {
        assertTrue(Demo.isTriangle(5,3,4));
    }

    @Test
    public void validtriangle90() {
        assertTrue(Demo.isTriangle(6,8,10));
    }

    @Test
    public void invalidtriangle1() {
        assertFalse(Demo.isTriangle(1,2,100));
    }

    @Test
    public void invalidtriangle2() {
        assertFalse(Demo.isTriangle(2,100,1));
    }

    @Test
    public void invalidtriangle100() {
        assertFalse(Demo.isTriangle(100,1,2));
    }

    @Test
    public void invalidtriangledouble1() {
        assertFalse(Demo.isTriangle(5,5,10));
    }
    
    @Test
    public void invalidtriangledouble2() {
        assertFalse(Demo.isTriangle(5,10,5));
    }
    
    @Test
    public void invalidtriangledouble3() {
        assertFalse(Demo.isTriangle(10,5,5));
    }
    
    @Test
    public void threezerosides() {
        assertFalse(Demo.isTriangle(0, 0, 0));
    }

    @Test
    public void onezerosides() {
        assertFalse(Demo.isTriangle(5, 9, 0));
    }

    @Test
    public void negativesides() {
        assertFalse(Demo.isTriangle(-1, -1, -1));
    }

    @Test
    public void equilateral() {
        assertTrue(Demo.isTriangle(3,3,3));
    }

    @Test
    public void isosceles() { 
        assertTrue(Demo.isTriangle(5,5,8));
    }

    @Test
    public void largesides() {
        assertTrue(Demo.isTriangle(10000000, 10000001, 20000000));
    }
    
    @Test
    public void verysmall() {
    	assertTrue(Demo.isTriangle(0.1, 0.1, 0.1));
    }
    
    @Test
    public void testMainMethod() {
        String simulatedInput = "3\n4\n5\n";
        System.setIn(new ByteArrayInputStream(simulatedInput.getBytes()));

        Demo.main(new String[]{});
    }
}
