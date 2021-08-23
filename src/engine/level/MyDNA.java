package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()


public class MyDNA extends DNA
{
	
	public int numGenes = 0; //number of genes

	// Return a new DNA that differs from this one in a small way.
	// Do not change this DNA by side effect; copy it, change the copy, and return the copy.
	public MyDNA mutate ()
	{
		MyDNA copy = new MyDNA();
		//YOUR CODE GOES BELOW HERE

		Random rand = new Random();
		String bank = "0123456789";

		int chromL = this.getChromosome().length();
		int val = rand.nextInt(10);
		int location = rand.nextInt(chromL);
		String blank = "";

		for (int i = 0; i < chromL; i++) {

			if(location == i){
				blank += bank.charAt(val);
			} else {
				blank += this.getChromosome().charAt(i);
			}
		}

		copy.setChromosome(blank);

		//YOUR CODE GOES ABOVE HERE
		return copy;
	}
	
	// Do not change this DNA by side effect
	public ArrayList<MyDNA> crossover (MyDNA mate)
	{
		ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
		//YOUR CODE GOES BELOW HERE

        int length= this.getChromosome().length();
        int first = this.getChromosome().length()/4;

        MyDNA felipe = new MyDNA();
        MyDNA nathalia = new MyDNA();

        String fel = this.getChromosome().substring(0, first) + mate.getChromosome().substring(first, 2 * first) + mate.getChromosome().substring(2 * first, 3 * first) + mate.getChromosome().substring(3 * first, mate.getChromosome().length());
        felipe.setChromosome(fel);
        String nat = mate.getChromosome().substring(0, first) + this.getChromosome().substring(first, 2 * first) +  this.getChromosome().substring(2 * first, 3 * first) + this.getChromosome().substring(3 * first, this.getChromosome().length());
		nathalia.setChromosome(nat);

        offspring.add(felipe);
        offspring.add(nathalia);


		//YOUR CODE GOES ABOVE HERE
		return offspring;
	}
	
	// Optional, modify this function if you use a means of calculating fitness other than using the fitness member variable.
	// Return 0 if this object has the same fitness as other.
	// Return -1 if this object has lower fitness than other.
	// Return +1 if this objet has greater fitness than other.
	public int compareTo(MyDNA other)
	{
		int result = super.compareTo(other);
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return result;
	}
	
	
	// For debugging purposes (optional)
	public String toString ()
	{
		String s = super.toString();
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return s;
	}
	
	public void setNumGenes (int n)
	{
		this.numGenes = n;
	}

}

